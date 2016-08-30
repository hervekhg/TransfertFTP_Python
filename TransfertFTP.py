#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Import des modules standard
# -----------------------------------------------------------------------------
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from glob import glob
import logging
from os.path import dirname, join
from sys import argv

# Import des modules non-standard
# -----------------------------------------------------------------------------
from resources.common.cnxftp import CConnexionFTP

# Chargement des constantes par défaut
# -----------------------------------------------------------------------------
execfile(join(dirname(argv[0]), "resources", "common", "_config.py"))

# Définition des constantes FTP Rennes
# -----------------------------------------------------------------------------
USER_1 = "ccovtom"
PASSWD_1 = "CCO&tom"
FTP_HOST1 = "172.23.115.128"
FTP_PORT1 = "21"

# Définition des constantes
# -----------------------------------------------------------------------------
TIMESTAMP = datetime.now().strftime("%Y%m%d")

# Définition des constantes pour les opérations FTP
# -----------------------------------------------------------------------------
# Exports Production : FTP RENNES -> Serveur RNS113WP
FIC_EXPORT_ = "*.tar" % TIMESTAMP
RNS_FTP_DIR_EXPORT_ = "Exports_"
LOCAL_DIR_EXPORT_ = "\input"  # A completer

# Exports Production : Serveur RNS113WP -> FTP Rennes
F_EXPORT = "*"
D_EXPORT = "exports"
LOCAL_DIR_EXPORT = "\output"  # A completer

# DumpBdd : Serveur RNS113WP -> FTP Rennes
FIC_DUMP_BDD = "7z.*"
DIR_DUMP= "DumpBdd"
LOCAL_DIR_DUMP = "\save"  # A completer


# Définition de la fonction principale
# -----------------------------------------------------------------------------
def main():
    logger = logging.getLogger(NOM_SCRIPT)
    logger.debug("Debut du script")
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("--all", dest="all", action="store_true",
                        help="Lance toutes les operations")
    parser.add_argument("--op", dest="operation", choices=map(str, range(1, 4)),
                        help="1. Download Exports Production (RNS -> Local)\n\
2. Upload Export Productions modifies (Local -> RNS)\n\
3. Upload Dump Bdd (Local -> RNS")
    logger.debug("Analyse des arguments")
    arguments = parser.parse_args(argv[1:])
    logger.debug("Options trouvees : %s", arguments)

    ftp_rns = CConnexionFTP(FTP_HOST1, FTP_PORT1, USER_1, PASSWD_1)

    if arguments.operation or arguments.all:
        # Exports de Production : FTP Rennes -> Serveur RNS113WP
        # ---------------------------------------------------------------------
        if int(arguments.operation) is 1 or arguments.all:
            logger.debug("Recuperation des Exports de Production")
            # Operation FTP Rennes -> Serveur RNS113WP
            ftp_rns.download(FIC_EXPORT_, LOCAL_DIR_EXPORT_,
                             RNS_FTP_DIR_EXPORT_, delete=True)

        # Exports de Production modifiés: Serveur RNS113WP -> FTP Rennes
        # ---------------------------------------------------------------------
        if int(arguments.operation) is 2 or arguments.all:
            logger.debug("Envoi des Exports de Productions modifies")
            ftp_rns.upload(glob(join(LOCAL_DIR_EXPORT, F_EXPORT)),
                           D_EXPORT, delete=True)

        # Dump Base de Données : Serveur RNS113WP -> FTP Rennes
        # ---------------------------------------------------------------------
        if int(arguments.operation) is 3 or arguments.all:
            logger.debug("Envoi du Dump de la Base de Donnees")
            ftp_rns.upload(glob(join(LOCAL_DIR_DUMP, FIC_DUMP_BDD)),
                           RNS_FTP_DIR_DUMP_BDD)
    logger.debug("Fin du script")

if __name__ == '__main__':
    main()
