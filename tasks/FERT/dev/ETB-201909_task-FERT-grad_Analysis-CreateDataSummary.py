# extractEV.py

# library of functions for checking, makeing, renaming files etc.
import os as os
# library for handelling data read in from a csv
import pandas as pd
import sys as sys

# https://pbpython.com/pathlib-intro.html
from pathlib import Path
import time
import numpy as np
# for printing dictionaries readable to the terminal
import pprint
# %**
# for catching the runtime warning which is raised by bad dprime calculations and not ordinarily caught by try/except
import warnings
warnings.filterwarnings("error")

# for timestamp of this analysis results
from datetime import datetime

# --------------------------------------------------------------------------
# MY FUNCTIONS

# creates the dictionary keys for each condition so the calculated values can be assigned dynamically
def updateDictForCond(condName):
    key_nTrails = 'nTrials_' + condName + '_tot'
    key_score = 'score_' + condName + '_tot'
    key_acc = 'acc_' + condName + '_mea'
    key_rt = 'rt_' + condName + '_mea'

    outp_px_emo[key_nTrails] = nTrials_emo
    outp_px_emo[key_score] = score_emo
    outp_px_emo[key_acc] = acc_emo
    outp_px_emo[key_rt] = rt_emo

    outp_px_emo.update(outp_px_emo_lev)

    translate = {}
    for k, v in outp_px_emo.items():
        newKey = k.replace('emo',condName)
        translate[k] = newKey

    for old, new in translate.items():
        outp_px_emo[new] = outp_px_emo.pop(old)

    return outp_px_emo

# creates the dictionary keys for each percentage emotion level so the calculated values can be assigned dynamically
def updateDictForLev(lev):
    key_nTrails = 'nTrials_emo_%03d' % lev
    key_score = 'score_emo_%03d' % lev
    key_acc = 'acc_emo_%03d' % lev
    key_rt = 'rt_emo_%03d' % lev

    outp_px_emo_lev[key_nTrails] = nTrials_emo_lev
    outp_px_emo_lev[key_score] = score_emo_lev
    outp_px_emo_lev[key_acc] = acc_emo_lev
    outp_px_emo_lev[key_rt] = rt_emo_lev

    return outp_px_emo_lev

def updateDictForCondMisclass(resp):
    key_misclass_resp = 'misclas_' + resp + '_tot'
    outp_px_misclas[key_misclass_resp] = misclass_resp

    return outp_px_misclas

# these functions were for Tereza's code where the correct keyes were wrong in the tiral order files.
# def calcScore(df,condName,keyCor):
#     calcdScore = df.key_respTrial_keys.str.count(keyCor).sum()
#     return calcdScore
# def calcScoreRev(df,condName,keyCor):
#     calcdScore = df.im_emotion.str.count(condName).sum()
#     return calcdScore


# --------------------------------------------------------------------------

# Set processing directory (intend to run this file from the analysis directory)
# where the results files are
# intention for this version is to run this once per directory
# https://stackoverflow.com/questions/27844088/python-get-directory-two-levels-up
dataRoot = Path.cwd().parents[0] / "data"
# dataRoot = Path.cwd() / "FERT_data_fullDataSet_Tereza_20191202"
dataRoot = Path(dataRoot)
print(' -- Analysing data from: ' + str(dataRoot))

# specify the task name (makes it easier to transfer this analysis code to another task)
task = 'FERT-grad'
print( ' -- Looking for task data for: ' + task)

# create a time stamp to attach to this run of the analysis.
# Enable useres to re-run the analysis at later stages with new participant info included
# (also super helpful for debugging)
analysisTimestamp = datetime.today().strftime('%y%m%d-%H%M%S')
# print(analysisTimestamp)


# where this analysis result file will be saved
resRoot = Path.cwd()
#resRoot.mkdir(parents=True, exist_ok=True)
fName_res = os.path.join(resRoot,task + '_summaryRes_' + analysisTimestamp + '.csv')
print(' -- This analysis will be saved with the filename: ' + fName_res)
# print(fName_res)

# input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

# list of conditions and correct keys which we'll loop through
# keys in the order of condition
listEmo_master = ['ang','dis','fea','hap','sad','sur','neu']
listKeyInp_master = ['z','x','c','v','b','n','m']

# arrays for storring values
# list of files to process
fList = []
outp_allPx = []
bigArray = pd.DataFrame()

# --------------------------------------------------------------------------

# START PROCESSING

# input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

# collect list of files to process
for i in dataRoot.glob('sub*' + task + '*.csv'):
    # print(i.name)
    fList.append((i.name, i.parent, time.ctime(i.stat().st_ctime)))

# create column headers for the outputs of the above search
columns = ["File_Name", "Parent", "Created"]
# create a data frame with the headers and fill wilth the search results
df = pd.DataFrame.from_records(fList, columns=columns)
# print(df.head())

# input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

# for each file (assume one per participant)
for index_px, p in df.iterrows():

    # create fresh arrays to store values for each participant, as we are building them with append
    # and don't want to accidentally stick new data onto old arrays
    outp_px = {}
    outp_px_emo = {}

    # --------------------------------------------------------------------------
    # get/set the files names for this participant

    # get the name of the file being processed
    path_bevavDat = dataRoot.joinpath(p.File_Name)

    parent = p.Parent
    # print(' -- Task results file directory:  ' + str(parent))
    outp_px['parentDir'] = parent

    # input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

    print(' -- Task results file:            ' + p.File_Name)
    outp_px['resFile'] = p.File_Name

    # now going to pull some useful information out of the file name and create an ev file name
    # 'split' the file name at the "_" character to get the first part, which we know to be pxID
    pxID = p.File_Name.split('_',1)[0]
    # print(' -- pxID:                         ' + pxID)
    outp_px['pxID'] = pxID

    # in the below split the filename into useful parents
    # without defining the maximum number of parts the stong should be split into
    # https://www.geeksforgeeks.org/python-string-split/
    # also using .strip to remove bits between the "-" seperators
    # IMPORTANT that this fits the results file structure, i.e. that index specified matches the part intended
    taskVerNum = p.File_Name.split('_')[3]
    outp_px['taskVerNum'] = taskVerNum

    rxVisitNum = p.File_Name.split('_')[4]
    outp_px['researchVisitNum'] = rxVisitNum

    year = p.File_Name.split('_')[5].strip('date-')
    outp_px['visitYear'] = year

    month = p.File_Name.split('_')[6]
    outp_px['visitMonth'] = month

    day = p.File_Name.split('_')[7]
    outp_px['visitDay'] = day

    time = p.File_Name.split('_')[8].strip('.csv')
    outp_px['visitTime'] = time

    # print(outp_px['resFile'])
    # print(outp_px['taskVerNum'])
    # print(outp_px['researchVisitNum'])
    # print(outp_px['visitYear'])
    # print(outp_px['visitMonth'])
    # print(outp_px['visitDay'])
    # print(outp_px['visitTime'])

    # --------------------------------------------------------------------------
    # begin processing the data!
    try:

        # read the data in
        behavDat = pd.read_csv(path_bevavDat)
        # rename some column headers form the original csv file as they have horrible dots in and we don't like random dots! (they mean something in python)
        behavDat.rename(columns={'loop_block.thisIndex':'loop_block_index',
                                'key_respTrial.keys':'key_respTrial_keys',
                                'key_respTrial.corr':'key_respTrial_corr',
                                'key_respTrial.rt': 'key_respTrial_rt',
                                'Research Visit Numer': 'ResearchVisitNumber',
                                'Study Code': 'StudyCode',
                                'Researcher Name': 'ResearcherName'},
                                inplace=True)

        # generate a lit of the emotion names present in the file
        # find the unique values (words) in that column
        # then remove the unique "nan" (this is just a loop written in a line)
        # better this way than assuming that all emotions were presented.
        listEmo_data = behavDat['im_emotion'].unique()
        listEmo_data = [x for x in listEmo_data if str(x) != 'nan']

        for cond in listEmo_data:
            # print(' -- Condition:                    ' + cond)
            # find the data where the contents of the im_emotion column matches the condition we're working in
            data_emo = behavDat[behavDat.im_emotion == cond]

            # ------------------------------------------------------------------
            # Process each emotion condition

            # total scores for each condition
            nTrials_emo = len(data_emo)

            # For Tereza's data, the correct keys weren't input correctly or consistantly onto the stimulus spreadsheets
            # Most notibly there were spaces in the "correct key" field which were never received as responses and in some cases the wrong key was specified in the spreadsheet
            # Having to calculate the score based on a count of the letters rather than reading off results files

            # this block was for Tereza's code where the correct keyes were wrong in the tiral order files.
            # if cond == 'anger':
            #     calcdScore = calcScore(data_emo,'ang','z')
            # elif cond == 'digust':
            #     calcdScore = calcScore(data_emo,'dis','x')
            # elif cond == 'fear':
            #     calcdScore = calcScore(data_emo,'fea','c')
            # elif cond == 'happy':
            #     calcdScore = calcScore(data_emo,'hap','v')
            # elif cond == 'sad':
            #     calcdScore = calcScore(data_emo,'sad','b')
            # elif cond == 'surprise':
            #     calcdScore = calcScore(data_emo,'sup','n')
            # elif cond == 'neutral':
            #     calcdScore = calcScore(data_emo,'neu','m')
            # score_emo = calcdScore

            score_emo = data_emo.key_respTrial_corr.sum()

            # print(' -- Score: ' + str(score_emo))
            # input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

            acc_emo = (score_emo/nTrials_emo)*100
            rt_emo = data_emo.key_respTrial_rt.mean()

            # get the number of percentage emotion levels
            nLev = data_emo['im_percentEmo'].unique()
            nLev = np.sort(nLev)

            # create a fresh arrays to store calculated values for each level
            outp_px_emo_lev = {}

            # ------------------------------------------------------------------
            # Process each level
            for lev in nLev:

                # print(' -- Percent emotion:              ' + str(lev))

                # get the data for that level
                data_lev = data_emo[data_emo.im_percentEmo == lev]
                # calculate teh variables for that level
                nTrials_emo_lev = len(data_lev)

                # this block was for Tereza's code where the correct keyes were wrong in the tiral order files.
                # if cond == 'anger':
                #     calcdScore = calcScore(data_lev,'ang','z')
                # elif cond == 'digust':
                #     calcdScore = calcScore(data_lev,'dis','x')
                # elif cond == 'fear':
                #     calcdScore = calcScore(data_lev,'fea','c')
                # elif cond == 'happy':
                #     calcdScore = calcScore(data_lev,'hap','v')
                # elif cond == 'sad':
                #     calcdScore = calcScore(data_lev,'sad','b')
                # elif cond == 'surprise':
                #     calcdScore = calcScore(data_lev,'sup','n')
                # elif cond == 'neutral':
                #     calcdScore = calcScore(data_lev,'neu','m')
                # score_emo_lev = calcdScore

                score_emo_lev = data_lev.key_respTrial_corr.sum()

                acc_emo_lev = (score_emo_lev/nTrials_emo_lev)*100
                rt_emo_lev = data_lev.key_respTrial_rt.mean()

                # use my function to store the calcualted values against the correct level key
                updateDictForLev(lev)

            # ----------------------------------------------------------------------
            # drop out of levels loop and back into condition to store the values

            # use my function to store the calcualted values against the correct condtion key
            if cond == 'anger':
                updateDictForCond('ang')
            elif cond == 'digust':
                updateDictForCond('dis')
            elif cond == 'fear':
                updateDictForCond('fea')
            elif cond == 'happy':
                updateDictForCond('hap')
            elif cond == 'sad':
                updateDictForCond('sad')
            elif cond == 'surprise':
                updateDictForCond('sur')
            elif cond == 'neutral':
                updateDictForCond('neu')

            # pprint.pprint(outp_px_emo)

        # add the condition info the the main dictioanry for that px
        outp_px.update(outp_px_emo)

        # --------------------------------------------------------------------------
        # loop to calculate miscalssifications
        outp_px_misclas = {}



        # how many times did you call something "sad", i.e. press one of the given response keys "r"

        # Tereza's version didn't have input key fields specified in a loop, therefore not so easy to read them from the csv.
        # Might be naughty and hard code them...
        # listKeyInp = listKeyInp_master

        listKeyInp = behavDat['key_inp'].unique()
        listKeyInp = [x for x in listKeyInp if str(x) != 'nan']

        # for keeping a running total of the number of misclassifications (percII)
        misclass_all_tot = 0

        for r in listKeyInp:

            # print(' -- Miscalssifications:           ' + r)
            data_keyInp = behavDat[behavDat.key_respTrial_keys == r]
            nTrials_resp = len(data_keyInp)

            # this block was for Tereza's code where the correct keyes were wrong in the tiral order files.
            # if r == 'z':
            #     calcdScore = calcScoreRev(data_keyInp,'anger','z')
            # elif r == 'x':
            #     calcdScore = calcScoreRev(data_keyInp,'digust','x')
            # elif r == 'c':
            #     calcdScore = calcScoreRev(data_keyInp,'fear','c')
            # elif r == 'v':
            #     calcdScore = calcScoreRev(data_keyInp,'happy','v')
            # elif r == 'b':
            #     calcdScore = calcScoreRev(data_keyInp,'sad','b')
            # elif r == 'n':
            #     calcdScore = calcScoreRev(data_keyInp,'surprise','n')
            # elif r == 'm':
            #     calcdScore = calcScoreRev(data_keyInp,'neutral','m')
            # corrTrials_resp = calcdScore

            corrTrials_resp = data_keyInp.key_respTrial_corr.sum()
            # print(corrTrials_resp)

            # input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

            misclass_resp = nTrials_resp - corrTrials_resp

            misclass_all_tot = misclass_all_tot + misclass_resp

            if r == 'z':
                updateDictForCondMisclass('ang')
            elif r == 'x':
                updateDictForCondMisclass('dis')
            elif r == 'c':
                updateDictForCondMisclass('fea')
            elif r == 'v':
                updateDictForCondMisclass('hap')
            elif r == 'b':
                updateDictForCondMisclass('sad')
            elif r == 'n':
                updateDictForCondMisclass('sur')
            elif r == 'm':
                updateDictForCondMisclass('neu')


        # --------------------------------------------------------------------------
        # drop out of the individual input key misclassifications to calculate percentages


        # calculate misclas emo percent I (number of misclas of each emotion out the the total number of misclas)
        # creating a new dict where the string _tot is replaced with _percI, and all values for those keys are treated with the same number formula
        tmpDict = {k.replace('_tot','_percI'):(v/misclass_all_tot)*100 for (k,v) in outp_px_misclas.items()}

        # store total number of miscallifications (doing this after so it doesn't do the above manipulation on the total)
        outp_px_misclas['misclass_all_tot'] = misclass_all_tot

        outp_px_misclas.update(tmpDict)

        # pprint.pprint(outp_px_misclas)

        # calculate the total number of trials for percII
        nTrials_tot = behavDat.time_trialEnd
        nTrials_tot = [x for x in nTrials_tot if str(x) != 'nan']
        nTrials_tot = len(nTrials_tot)
        # print(' -- nTrials_total: ' + str(nTrials_tot))

        outp_px_misclas['nTrials_tot'] = nTrials_tot

        outp_px.update(outp_px_misclas)

        # pprint.pprint(outp_px)

        out_px_sigDet = {}

        for c in listEmo_master:
            key_misclass_emo_tot = 'misclas_' + c + '_tot'
            key_nTrials_emo_tot = 'nTrials_' + c + '_tot'
            key_misclas_emo_percII = 'misclas_' + c + '_percII'

            # percII = (number of misclass for that emotion / (total number of trials - the number of trials that were that emotion))*100
            # i.e. = (number if times you got it wrong / number of times you could have got it wrong)*100
            outp_px[key_misclas_emo_percII] = (outp_px[key_misclass_emo_tot] / (outp_px['nTrials_tot'] - outp_px[key_nTrials_emo_tot]))*100

            # print(' -- Cond: ' + c)
            # print(' -- misclass: ' + str(outp_px[key_misclass_emo_tot]))
            # print(' -- nTrials not cond: ' + str(outp_px['nTrials_tot'] - outp_px[key_nTrials_emo_tot]))
            # print(' -- percII: ' + str(outp_px[key_misclas_emo_percII]))

            # --------------------------------------------------------------------------
            # signal detection
            key_sigDet_hit_emo  = 'sigDet_hit_' + c
            key_sigDet_fal_emo  = 'sigDet_fal_' + c
            key_sigDet_beta_emo = 'sigDet_beta_' + c
            key_sigDet_dpri_emo = 'sigDet_dpri_' + c

            hit_emo = outp_px['score_' + c + '_tot']/outp_px[key_nTrials_emo_tot]

            # print('score: ' + str(outp_px['score_' + c + '_tot']))
            # print('ntrials_emo: ' + str(outp_px[key_nTrials_emo_tot]))

            fal_emo = outp_px['misclas_' + c + '_tot']/(outp_px['nTrials_tot'] - outp_px[key_nTrials_emo_tot])

            # print(' -- hit rate: ' + str(hit_emo))
            # print(' -- false alarm: ' + str(fal_emo))

            try:
                beta_emo  = (hit_emo*(1-hit_emo) - fal_emo*(1-fal_emo)) / (hit_emo*(1-hit_emo) + fal_emo*(1-fal_emo))
            except Exception as e:
                print(' -- !! WARNING: beta was -inf for this data file. Entering value "nan" in aggregated results')
                beta_emo = float('nan')
            # print(' -- beta: ' + str(beta_emo))

            # input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

            try:
                dpri_emo = 0.5 + (((hit_emo - fal_emo)*(1 + hit_emo - fal_emo))/((4*hit_emo)*(1 - fal_emo)))
            except Exception as e:
                print(' -- !! WARNING: dprime was -inf for this data file. Entering value "nan" in aggregated results')
                dpri_emo = float('nan')
            # print(' -- dprime: ' + str(dpri_emo))

            # input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

            out_px_sigDet[key_sigDet_hit_emo] = hit_emo
            out_px_sigDet[key_sigDet_fal_emo] = fal_emo
            out_px_sigDet[key_sigDet_beta_emo] = beta_emo
            out_px_sigDet[key_sigDet_dpri_emo] = dpri_emo

            # input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

        # --------------------------------------------------------------------------
        # drop out of condition loop (into participant loop) to collate the data

        outp_px.update(out_px_sigDet)

        # print('-- pxDict:')
        # pprint.pprint(outp_px)

        # This was a really hacky way of turning the dictionary into a data frame,
        # then transposing it, then setting the column headers as the transposed first row
        tmp = pd.DataFrame(list(outp_px.items()))
        tmp=tmp.transpose()
        tmp.columns = tmp.iloc[0]
        tmp = tmp.drop([tmp.index[0]])

        # print(' -- particpant index: ' + str(index_px))
        # print(' -- pxArray size:                 ' + str(tmp.shape))
        # print(tmp)

        # input('\n ** PRESS ANY KEY TO CONTINUE (ctrl+C to quit) **')

        if index_px == 0:
            bigArray=tmp
        else:
            # %**
            # getting an error when the px arrays aren't the same size (raised because an eary version of the task has incorrect trial order files)
            # bigArray=bigArray.append(tmp)
            bigArray=bigArray.append(tmp,sort=False)

        # print(' -- bigArray:')
        # print(bigArray)

    # https://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
    except Exception as e:
        print(' -- !! WARNING: Could not process this data. Skipping file.')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(' -- !! WARNING: Specified error: ' + str(e) + ' line: ' + str(exc_tb.tb_lineno))
        continue


# print(' -- bigArray reindexed:')

bigArray = bigArray.reset_index(drop=True)

# print(bigArray)

print(' -- Saving all accuracy results to:                    ' + fName_res)
bigArray.to_csv(fName_res)
