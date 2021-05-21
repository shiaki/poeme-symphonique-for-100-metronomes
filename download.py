
qstr = '''https://wis-tns.weizmann.ac.il/search?&page={:d}&discovered_period_units=years&unclassified_at=0&classified_sne=0&include_frb=0&name_like=0&isTNS_AT=all&public=all&coords_unit=arcsec&reporting_groupid%5B%5D=null&groupid%5B%5D=null&classifier_groupid%5B%5D=null&objtype%5B%5D=null&at_type%5B%5D=null&date_start%5Bdate%5D={:d}-01-01&date_end%5Bdate%5D={:d}-12-31&discovery_instrument%5B%5D=null&classification_instrument%5B%5D=null&associated_groups%5B%5D=null&frb_repeat=all&frb_measured_redshift=0&num_page=500&display%5Bredshift%5D=1&display%5Bhostname%5D=1&display%5Bhost_redshift%5D=1&display%5Bsource_group_name%5D=1&display%5Bclassifying_source_group_name%5D=1&display%5Bdiscovering_instrument_name%5D=1&display%5Bclassifing_instrument_name%5D=1&display%5Bprograms_name%5D=1&display%5Binternal_name%5D=1&display%5BisTNS_AT%5D=1&display%5Bpublic%5D=1&display%5Bend_pop_period%5D=1&display%5Bspectra_count%5D=1&display%5Bdiscoverymag%5D=1&display%5Bdiscmagfilter%5D=1&display%5Bdiscoverydate%5D=1&display%5Bdiscoverer%5D=1&display%5Bremarks%5D=1&display%5Bsources%5D=1&display%5Bbibcode%5D=1&display%5Bext_catalogs%5D=1&format=csv'''

year_begin, year_end = 2020, 2020
for i in range(75):
    qstr_t = qstr.format(i, year_begin, year_end)
    print('''wget -O Part-{:02d}.csv '{:s}' '''.format(i, qstr_t,))
