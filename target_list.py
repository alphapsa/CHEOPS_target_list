# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 08:47:03 2024

    This module is created to help generate target list .csv-files
    that are used by CHEOPS GTO programmes. The idea is that given
    a target name the auxliary data, such as the Gaia DR2 ID, 
    G magnitude, coordinates, etc can be retrieved from simbad
    and put into the desired comma-separated format.

@author: Alexis Brandeker (alexis@astro.su.se)
"""

from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, get_sun, get_icrs_coordinates
from astroquery.simbad import Simbad


def make_csv_str(target_name, n_orbits=None, reserved=False):
    """Given a target name, queries SIMBAD and constructs a .csv
    string to be used for the CHEOPS GTO target list.
    n_orbits is the number of orbits to be observed, and 'reserved'
    if the target is to be reserved. Returns a single string.
    """
    
    if n_orbits is None:
        norb_str = '##'
    else:
        norb_str = str(n_orbits)
        
    if reserved:
        res_str = 'y'
    else:
        res_str = 'n'
    
    dr2 = get_DR2(target_name)
    Gmag = get_Gaia_mag(target_name)
    target_coo = get_icrs_coordinates(target_name, cache=True)
    ra_str, dec_str = radec_str(target_coo)

    max_angle = max_solar_angle_from_coo(target_coo)
    
    if max_angle < 110*u.deg: # This is unlikely to ever be observable by CHEOPS
        sea120 = '{:.1f} < 110 deg !!!!!'.format(max_angle)        
    elif max_angle < 120*u.deg: # This requires SEA relaxation
        sea120 = 'y'
    else:                       # All good
        sea120 = 'n' 
    
    ret_str = '{:s}, DR2 {:s}, {:s}, {:s}, {:.2f}, {:s}, {:s}, {:s}'.format(
        target_name, dr2, ra_str, dec_str, Gmag, norb_str, res_str, sea120)

    return ret_str


def get_DR2(target_name):
    """Returns Gaia DR2 ID, if it exists.
    (queries simbad)    
    """
    # The Simbad querying object
    simbad = Simbad()
    simbad.ROW_LIMIT = -1

    result = simbad.query_objectids(target_name)
    for name in result["ID"]:

        if "Gaia DR2" in name:
            splitted = name.split('Gaia DR2')
            if splitted[0] == "":
                number = int(splitted[1])
                return str(number)
    # If nothing is found, return None
    return None    


def get_Gaia_mag(target_name):
    """Returns Gaia G magnitude given target name
    (queries simbad)
    """
    customSimbad = Simbad()
    customSimbad.add_votable_fields('flux(G)')
    res_tab = customSimbad.query_object(target_name)
    return res_tab['FLUX_G'][0]

    
def radec_str(target_coo):
    """Returns formatted strings of RA and DEC
    """
    ra_str = target_coo.ra.to_string(u.hour, sep=':', precision=2)
    dec_str = target_coo.dec.to_string(u.deg, sep=':', alwayssign=True, precision=1)
    return ra_str, dec_str


def max_solar_angle_from_coo(target_coo):
    """Given target coordinates, computes the maximum angle between the
    coordinates and the Sun. Returns maximum angle in degrees.
    """
    new_year = Time('2001-01-01')
    max_sep = -1*u.deg

    for n in range(1,365):
        date = new_year + n*u.day
        sun_gcrs = get_sun(date)
        sun_icrs = SkyCoord(ra=sun_gcrs.ra, dec=sun_gcrs.dec)
        sep = target_coo.separation(sun_icrs)        
        if max_sep < sep:
            max_sep = sep
    return max_sep


def max_solar_angle(target_name):
    """Given target_name, computes the maximum angle between the target and the
    Sun. Returns maximum angle in degrees.
    """
    target_coo = get_icrs_coordinates(target_name, cache=True)
    return max_solar_angle_from_coo(target_coo)


if __name__ == '__main__': 

# Example: We want to observe the reserved target 55 Cnc with 15 orbits

    target_str = make_csv_str('55 Cnc', n_orbits=15, reserved=True)
    
    # target_str now contains:
    # "55 Cnc, DR2 704967037090946688, 8:52:35.81, +28:19:51.0, 5.73, 15, y, n"
        
    print(target_str)
    
