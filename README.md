ects
====

## What is this?

A write-only, versioned-by-default file backup system.
(I like the sound of buzzwords in the morning.)

This is for a school computer lab setting, where students need to back their work up to a central server for grading and the like as well as for simple redundant backup purposes, considering that multiple students share a user on the computer and sometimes ... things ... happen to people's files.

## What does it do?

If a folder is backed up, every file of the form `folder/path/to/file.ext` is backed up to `uploads/username/folder/path/to/file.ext/hash.ext` on the server, where `hash` is the `sha256` hash of the file contents.

For instance, I created a few folders and some empty Word files in Documents on a Windows machine, with very creative names, and backed them up. The paths on the server correspond to the source paths as follows:

`Documents/New Folder/New Microsoft Word Document - Copy (13).docx -> uploads/asdf/Documents/New folder/New Microsoft Word Document - Copy (13).docx/d41d8cd98f00b204e9800998ecf8427e.docx`

If the file is changed, a new file is created in `/folder/path/to/file/newhash.txt` where `newhash` is, predictably, the new hash of the file.

## How do I set it up?

This depends on whether you're trying to run a client or a server.

### Server

Install the following `pip` packages:

* `flask` - the web server that we use to serve up what is essentially a REST API
* `coloredlogs` - for blingy hax0r logging, although this isn't currently working on Windows (I wonder why)

This is done with the following incantation:

`> pip install flask coloredlogs`

Now navigate to the `ects/server` directory and run

`> python server.py`

or even just `> ./server.py` (or double-click the `server.py` file) if the execute bit is set.

### Client

Ideally, you'd want to create an executable with PyInstaller, which bundles all the code and dependencies into a single `.exe` file that you can copy and paste to all your client machines. (Or, you know, actually have sense and use some kind of DevOps tools ... but where we're going, we don't need any of that.)

Install the `pyinstaller` package first:

`> pip install pyinstaller`

Now you want to get the dependencies, which should consist of nothing but `requests`. For some reason, the latest version of `requests` doesn't play nice with PyInstaler, so we'll just get version `2.5.1`:

`> pip install requests==2.5.1`

Navigate to the `client` folder:

`> cd ects/client`

and run `pyinstaller`:

`> pyinstaller -F -w filechooser.py`

This will create an executable in `ects/client/dist`, named `filechooser.exe`, that you can use as a standalone executable on any machine. Note that the executable is highly dependent on OS, architecture, and so on. So generating an executable on a 64-bit Windows 10 and trying to run it on x84 machines running Windows XP is a bad idea. (I'm speaking from experience here.)
