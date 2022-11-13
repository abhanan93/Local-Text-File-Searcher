import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import whoosh.index as index

old = 0
class MyHandler(FileSystemEventHandler):
    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            ix = index.open_dir("indexdir")
            ix.delete_by_term("path", event.src_path)
            ix.close()

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            ix = index.open_dir("indexdir")
            writer = ix.writer()
            fp = open(event.src_path,'rb')
            text = fp.read().decode(errors='replace')
            writer.add_document(title=event.src_path.split("\\")[-1], path=event.src_path,\
            content=text)
            fp.close()
            writer.commit()

    def on_modified(self, event):
        global old
        if event.is_directory:
            pass
        else:
            statbuf = os.stat(event.src_path)
            new = statbuf.st_mtime
            if (new - old) > 0.5:
                print("Received modified event - %s." % event.src_path)
                ix = index.open_dir("indexdir")
                writer = ix.writer()
                fp = open(event.src_path,'rb')
                text = fp.read().decode(errors='replace')
                writer.update_document(title=event.src_path.split("\\")[-1], path=event.src_path,\
                content=text)
                fp.close()
                writer.commit()
            old = new


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='corpus', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()