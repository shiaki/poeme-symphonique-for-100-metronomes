
import os, sys, glob, json
from collections import OrderedDict
import numpy as np
from astropy.io import fits

output_name = '../TNS-MasterCatalog-Full'

if __name__ == '__main__':

    # parse csv files
    rows, header = list(), None
    for file_i in glob.glob('./**/Part-??.csv'):
    # for file_i in glob.glob('./Part-??.csv'):
        with open(file_i, 'r') as f: rows_i = f.readlines()
        if not header: header = rows_i[0].strip()[1:-1].split('","')
        rows_i = [w.strip() for w in rows_i if '"ID","Name"' not in w]
        rows.extend(rows_i)
    rows = [w[1:-1].split('","') for w in sorted(rows)]

    # replace header string.
    header = [w.lower().replace('/s', 's').replace('/', '_' \
              ).replace('. ', '_').replace(' (ut)', '').replace(' ', '_') \
              for w in header]

    # convert to table.
    as_float    = lambda x: float(x) if x else np.nan
    as_int      = lambda x: int(x) if x else -1
    identi      = lambda x: x.strip()

    unicode2ascii = lambda x: x.encode( \
            encoding='ascii', errors='backslashreplace').decode().strip()

    sexagesimal = [1, 1. / 60., 1. / 3600.]
    dms_to_deg  = lambda x: (-1. if ('-' in x) else 1.) * np.dot(np.abs( \
            [float(w) for w in x.split(':')]), sexagesimal)
    hms_to_deg  = lambda x: np.abs(15. * dms_to_deg(x))

    cols = [
        ('id',                      'i4',   as_int),
        ('name',                    'S',    identi),
        ('ra',                      'f8',   hms_to_deg),
        ('dec',                     'f8',   dms_to_deg),
        ('obj_type',                'S',    identi),
        ('redshift',                'f4',   as_float),
        ('host_name',               'S',    unicode2ascii),
        ('host_redshift',           'f4',   as_float),
        ('reporting_groups',        'S',    identi),
        ('discovery_data_sources',  'S',    identi),
        ('classifying_groups',      'S',    identi),
        ('associated_groups',       'S',    identi),
        ('disc_internal_name',      'S',    identi),
        ('disc_instruments',        'S',    identi),
        ('class_instruments',       'S',    identi),
        ('tns_at',                  'i4',   as_int),
        ('public',                  'i4',   as_int),
        ('end_prop_period',         'S',    identi),
        ('discovery_mag_flux',      'f4',   as_float),
        ('discovery_filter',        'S',    identi),
        ('discovery_date',          'S',    identi),
        ('sender',                  'S',    unicode2ascii),
        ('remarks',                 'S',    identi),
        ('ext_catalogs',            'S',    identi)
    ]

    # convert things.
    N_rows, max_len = len(rows), dict()
    for i_col, (col_i, dtp_i, conv_i) in enumerate(cols):
        if dtp_i == 'S':
            max_len[col_i] = np.max([ \
                    len(unicode2ascii(rows[k][i_col])) \
                    for k in range(N_rows) \
            ])
            # continue
        for k in range(N_rows):
            rows[k][i_col] = conv_i(rows[k][i_col])

    # create data type.
    dtp = list()
    round_4 = lambda x: x + 4 - x % 4
    for col_i, dtp_i, _ in cols:
        if dtp_i == 'S': dtp_i = 'S{:d}'.format(round_4(max_len[col_i]))
        dtp.append((col_i, dtp_i))

    # create new table.
    cat = np.zeros(N_rows, dtype=dtp)
    for i_row, row_i in enumerate(rows): cat[i_row] = tuple(row_i)

    # save.
    np.save(output_name, cat)
    fits.writeto(output_name + '.fits', cat, overwrite=True)

    rows_dict = [{k: v for k, v in zip(header, w)} for w in rows]
    with open(output_name + '.json', 'w') as f:
        json.dump(rows_dict, f, indent=4)
