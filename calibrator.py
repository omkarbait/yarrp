# This module contains several flagging recipes.
import subprocess
import casatasks as cts


def delaycal(msfile, params, field=None):

    refant = params['flagging']['refant']
    caltable = params['calibration']['delaytable']
    gaintables = params['calibration']['gaintables']
    uvran = params['general']['uvran']

    cts.gaincal(msfile, field=field, solint='60s',  spw='0', uvrange=uvran, refant=refant, caltable=caltable, gaintype='K', solnorm=True, gaintable=gaintables, parang=True)
    return print('Delay calibration done')

def bpasscal(msfile, params, field=None):
    
    refant = params['flagging']['refant']
    bpassgaintable = params['calibration']['bpassgaintable']
    bpasstable = params['calibration']['bpasstable']
    gaintables = params['calibration']['gaintables']
    uvran = params['general']['uvran']

    #Initial gain calibration
    cts.gaincal(msfile, caltable=bpassgaintable, field=field, uvrange=uvran, spw ='0', solint = 'int', solmode='R', refant = refant, minsnr = 2.0, gaintype = 'G', calmode = 'ap', gaintable = gaintables, interp = ['linear, linear',], append=True, parang = False)
    gaintables.append(bpassgaintable)
    print(gaintables, 'before bpass')
    # bpass calibration
    cts.bandpass(msfile, caltable=bpasstable, spw ='0', field=field, uvrange=uvran,  solint='inf', refant=refant, solnorm = True, minsnr=2.0, append=True, fillgaps=8, parang = False, gaintable= gaintables, interp=['linear,linear','linear,linear'])
    #cts.bandpass(msfile, caltable=bpasstable, spw ='0', field=field, solint='inf', refant=refant, solnorm = True, minsnr=2.0, fillgaps=8, bandtype='BPOLY', degamp=5, degphase=7, parang = True, gaintable=gaintables, interp=['nearest,nearestflag','nearest,nearestflag'])

    # Removing and also deleting the on-the fly gaincal table used for bandpass
    subprocess.run('rm -r {}'.format(bpassgaintable), shell=True, check=True) 
    gaintables.remove(bpassgaintable)

    return print('Bandpass calibration done')

# The main amplitude and phase calibrator
def apcal(msfile, params, field=None):
    refant = params['flagging']['refant']
    gaintables = params['calibration']['gaintables']
    apgaintable = params['calibration']['apgaintable'] 
    uvran = params['general']['uvran']
    spw = params['general']['spw']     

    print(gaintables, 'before ampcal')
    cts.gaincal(vis=msfile, caltable= apgaintable, spw=spw, append=True, field=field, uvrange=uvran, solint = '60s',refant = refant, minsnr = 3.0, gaintype = 'G', calmode = 'ap', solmode='R', gaintable = gaintables, interp = ['linear, linear', 'linear, linear'], parang=True)

    return print('Amplitude and phase calibration done for ', field)

def selfcal(msfile, params, mode='p', in_gaintable=[], out_gaintable='sc_p.test.gcal', solint='8min', solnorm=False):
    refant = params['flagging']['refant']
    #print(gaintables, 'before selfcal') 
    cts.gaincal(msfile, caltable=out_gaintable, append=False, field='0', spw='0', uvrange='', solint = solint, refant = refant, minsnr = 2.0, gaintype = 'G', solnorm= solnorm, calmode = 'p', solmode='R', gaintable = in_gaintable, interp = ['linear, linear'], parang = True)
    return None 