Solution = {'Conx': ['AUD', 'DHU', 'DHUM', 'DHUH', 'ETCM', 'PAK', 'TCA'],
            'Platform': ['BBS', 'BCMA', 'CCMB', 'DDM', 'FMDM', 'NFCA', 'PDM', 'POT', 'PSCM', 'RBCM', 'RDDM', 'RPDM', 'SUM', 'TRM'],
            'Propulsion': ['GCCC', 'GHCA', 'HLCM', 'HVBM', 'IHFA', 'IHRA', 'TVRL', 'TVRR'],
            'SVA': ['FSRR', 'RSRL', 'RSRR', 'SRS', 'SRSM', 'SRSR', 'ADPU', 'FLL', 'FLR', 'FLCW'],
            'SWEP': ['ADSS','FIOC', 'HIA', 'HIB', 'HIC', 'HPA', 'HPB', 'LPA', 'LPC', 'FGWA', 'FGWM','PGWA', 'PGWM', 'PGWX', 'PPD', 'SGA', 'VESC', 'BPD', 'DGWA', 'DGWM'],
            'Tophat': ['BTLL', 'BTLR', 'CSD', 'DLPR', 'DLPL', 'HCML', 'HCMR', 'HOD', 'HUD', 'OHC', 'OHLC', 'OHRL', 'OHRR', 'OHTL', 'OHTR', 'PSMD', 'PSMP', 'RML', 'RMR', 'SWM', 'TTLL', 'TTLR', 'WPC', 'CRSM'],
            'ME': ['ALL', 'ECOS', 'FAS', 'Vehicle']
            }

ECUs = {'AUD': 'Conx', 'DHU': 'Conx', 'DHUM': 'Conx', 'DHUH': 'Conx', 'ETCM': 'Conx', 'PAK': 'Conx', 'TCA': 'Conx', 'BBS': 'Platform', 'BCMA': 'Platform', 'CCMB': 'Platform', 'DDM': 'Platform', 'FMDM': 'Platform', 'NFCA': 'Platform', 'PDM': 'Platform', 'POT': 'Platform', 'PSCM': 'Platform', 'RBCM': 'Platform', 'RDDM': 'Platform', 'RPDM': 'Platform', 'SUM': 'Platform', 'TRM': 'Platform', 'GCCC': 'Propulsion', 'GHCA': 'Propulsion', 'HLCM': 'Propulsion', 'HVBM': 'Propulsion', 'IHFA': 'Propulsion', 'IHRA': 'Propulsion', 'TVRL': 'Propulsion', 'TVRR': 'Propulsion', 'FSRR': 'SVA', 'ADPU': 'SVA', 'RSRL': 'SVA', 'RSRR': 'SVA', 'SRS': 'SVA', 'SRSM': 'SVA', 'SRSR': 'SVA', 'FIOC': 'SWEP', 'PGWX': 'SWEP', 'HIA': 'SWEP', 'HIB': 'SWEP', 'HIC': 'SWEP', 'HPA': 'SWEP', 'HPB': 'SWEP', 
'LPA': 'SWEP', 'LPC': 'SWEP', 'PGWA': 'SWEP', 'PGWM': 'SWEP', 'BPD': 'SWEP', 'PPD': 'SWEP', 'SGA': 'SWEP', 'DGWA': 'SWEP', 'VESC': 'SWEP', 'DLPR': 'Tophat', 'HCML': 'Tophat', 'HCMR': 'Tophat', 'HOD': 'Tophat', 'HUD': 'Tophat', 'OHC': 'Tophat', 'OHLC': 'Tophat', 'OHRL': 'Tophat', 'OHRR': 'Tophat', 'OHTL': 'Tophat', 'OHTR': 'Tophat', 'PSMD': 'Tophat', 'PSMP': 'Tophat', 'RML': 'Tophat', 'RMR': 'Tophat', 'SWM': 'Tophat', 'TTLL': 'Tophat', 'TTLR': 'Tophat', 'WPC': 'Tophat', 'CRSM': 'Tophat', 'CSD': 'Tophat', 'FLL': 'SVA', 'FLR': 'SVA', 'FLCW': 'SVA', 'ADSS': 'SWEP', 'FGWA': 'SWEP', 'FGWM': 'SWEP', 'DGWM': 'SWEP', 'BTLL': 'Tophat', 'BTLR': 'Tophat', 'DLPL': 
'Tophat', 'ALL': 'ME', 'ECOS': 'ME', 'FAS': 'ME', 'Vehicle': 'ME'}

ECU_list = ['AUD', 'DHU', 'DHUM', 'DHUH', 'ETCM', 'PAK', 'TCA', 'BBS', 'BCMA', 'CCMB', 'DDM', 'FMDM', 'NFCA', 'PDM', 'POT', 'PSCM', 'RBCM', 'RDDM', 'RPDM', 'SUM', 'TRM', 'GCCC', 'GHCA', 'HLCM', 'HVBM', 'IHFA', 'IHRA', 'TVRL', 'TVRR', 'FSRR', 'ADPU', 'RSRL', 'RSRR', 'SRS', 'SRSM', 'SRSR', 'FIOC', 'PGWX', 'HIA', 'HIB', 'HIC', 'HPA', 'HPB', 'LPA', 'LPC', 'PGWA', 'PGWM', 'BPD', 'PPD', 'SGA', 'DGWA', 'VESC', 'DLPR', 'HCML', 'HCMR', 'HOD', 'HUD', 'OHC', 'OHLC', 'OHRL', 'OHRR', 'OHTL', 'OHTR', 'PSMD', 'PSMP', 'RML', 'RMR', 'SWM', 'TTLL', 'TTLR', 'WPC', 'CRSM', 'CSD', 'FLL', 'FLR', 'FLCW', 'ADSS', 'FGWA', 'FGWM', 'DGWM', 'BTLL', 'BTLR', 'DLPL', 'ALL', 'ECOS', 'FAS', 'Vehicle']
# for key, value in Solution.items():
#     for i in value:
#         ECUs[i] = key
# print(ECUs)