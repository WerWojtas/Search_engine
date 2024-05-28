from installer import Installer
import compileall

compileall.compile_dir('.', force=True)


install = Installer()
install.scrap()
install.parse()
install.find_terms()
install.create_matrixes()
