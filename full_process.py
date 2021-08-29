
global_vars = {'DEST':'pdfs/', 'ZIP_PATH':'zips/'}

def execfile(file):
    with open(file) as f:
        code = compile(f.read(), file, 'exec')
        exec(code, global_vars)

if __name__=='__main__':
    execfile('ripper.py')
    execfile('downloader.py')
    # run unzipper.py
    # then run totext.py
