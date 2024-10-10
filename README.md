# CHEOPS_target_list
Uses SIMBAD queries to simplify the creation of CHEOPS GTO programme .csv-file target lists
according to template v0.5:

 target name, Gaia DR2 identifier, right ascension [hh:mm:ss.ss], declination [+/-dd:mm:ss.s], G mag, total number of orbits, reserved [y/n], Sun excl. angle < 120 [y/n]

INSTALL:
Needs astropy and astroquery modules. Single .py-file, copy it to favourite location.

EXAMPLE:

    # We want to observe the reserved target 55 Cnc with 15 orbits
    
    target_str = make_csv_str('55 Cnc', n_orbits=15, reserved=True)
    
    # target_str now contains:
    # "55 Cnc, DR2 704967037090946688, 8:52:35.81, +28:19:51.0, 5.73, 15, y, n"
    
