from django.db import models

# Create your models here.


class AuthUserTab(models.Model):
    id_number = models.FloatField(primary_key=True, unique=True)
    token_key = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Auth_User_Tab'


class FcpFamilyMemberTab(models.Model):
    f_m_id = models.FloatField(primary_key=True)
    sample_id = models.FloatField()
    member_no = models.FloatField()
    member_name = models.CharField(max_length=250, blank=True, null=True)
    member_name_first = models.CharField(max_length=250, blank=True, null=True)
    member_name_second = models.CharField(max_length=250, blank=True, null=True)
    member_name_third = models.CharField(max_length=250, blank=True, null=True)
    id_number_member = models.FloatField(blank=True, null=True)
    family_relation = models.FloatField(blank=True, null=True)
    gender = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    birth_month = models.FloatField(blank=True, null=True)
    birth_year = models.FloatField(blank=True, null=True)
    nationality = models.FloatField(blank=True, null=True)
    nationality_txt = models.CharField(max_length=250, blank=True, null=True)
    difficulty_1 = models.FloatField(blank=True, null=True)
    difficulty_1_degree = models.FloatField(blank=True, null=True)
    difficulty_2 = models.FloatField(blank=True, null=True)
    difficulty_2_degree = models.FloatField(blank=True, null=True)
    difficulty_3 = models.FloatField(blank=True, null=True)
    difficulty_3_degree = models.FloatField(blank=True, null=True)
    difficulty_4 = models.FloatField(blank=True, null=True)
    difficulty_4_degree = models.FloatField(blank=True, null=True)
    difficulty_5 = models.FloatField(blank=True, null=True)
    difficulty_5_degree = models.FloatField(blank=True, null=True)
    difficulty_6 = models.FloatField(blank=True, null=True)
    difficulty_6_degree = models.FloatField(blank=True, null=True)
    difficulty_7_txt = models.CharField(max_length=250, blank=True, null=True)
    difficulty_7_degree = models.FloatField(blank=True, null=True)
    difficulty_8 = models.FloatField(blank=True, null=True)
    place_birth = models.FloatField(blank=True, null=True)
    place_stay_previous = models.FloatField(blank=True, null=True)
    place_stay = models.FloatField(blank=True, null=True)
    study_status = models.FloatField(blank=True, null=True)
    education_status = models.FloatField(blank=True, null=True)
    study_field = models.FloatField(blank=True, null=True)
    marital_status = models.FloatField(blank=True, null=True)
    males_count = models.FloatField(blank=True, null=True)
    females_count = models.FloatField(blank=True, null=True)
    labor_status = models.FloatField(blank=True, null=True)
    labor_status_txt = models.CharField(max_length=250, blank=True, null=True)
    main_job = models.FloatField(blank=True, null=True)
    economic_activity = models.FloatField(blank=True, null=True)
    work_sector_type = models.FloatField(blank=True, null=True)
    work_sector_type_txt = models.CharField(max_length=250, blank=True, null=True)
    t_start_date = models.DateField(blank=True, null=True)
    t_end_date = models.DateField(blank=True, null=True)
    t_update_date = models.DateField(blank=True, null=True)
    member_status = models.FloatField(blank=True, null=True)
    member_delete_status = models.FloatField(blank=True, null=True)
    insert_by = models.FloatField(blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    update_by = models.FloatField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fcp_family_member_tab'


class GenLookupListView(models.Model):
    rp_id = models.FloatField(blank=True, null=True, primary_key=True)
    column_name = models.CharField(max_length=250, blank=True, null=True)
    lookup_id = models.FloatField()
    lookup_name = models.CharField(max_length=255, blank=True, null=True)
    lookup_name_en = models.CharField(max_length=255, blank=True, null=True)
    l_active = models.FloatField(blank=True, null=True)
    lookup_list_id = models.FloatField()
    list_name = models.CharField(max_length=1000, blank=True, null=True)
    seq_no = models.FloatField(blank=True, null=True)
    l_list_active = models.FloatField(blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    ref_work_type_pk = models.FloatField(blank=True, null=True)
    list_name_en = models.CharField(max_length=1000, blank=True, null=True)
    col_type = models.FloatField(blank=True, null=True)
    col1 = models.CharField(max_length=500, blank=True, null=True)
    col2 = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.lookup_name

    class Meta:
        managed = False
        db_table = 'gen_lookup_list_view'


class FcpFamilyDeathTab(models.Model):
    f_m_id = models.FloatField(primary_key=True)
    sample_id = models.FloatField(blank=True, null=True)
    member_no = models.FloatField(blank=True, null=True)
    member_name = models.CharField(max_length=250, blank=True, null=True)
    gender = models.FloatField(blank=True, null=True)
    nationality = models.FloatField(blank=True, null=True)
    death_age = models.FloatField(blank=True, null=True)
    reason_death = models.FloatField(blank=True, null=True)
    reason_death_txt = models.CharField(max_length=250, blank=True, null=True)
    member_status = models.FloatField(blank=True, null=True)
    member_delete_status = models.FloatField(blank=True, null=True)
    insert_by = models.FloatField(blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    update_by = models.FloatField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fcp_family_death_tab'


class FcpFamilyTab(models.Model):
    sample = models.ForeignKey('GenSampleTab', models.DO_NOTHING,)
    housing_type = models.FloatField(blank=True, null=True)
    housing_type_txt = models.CharField(max_length=250, blank=True, null=True)
    building_material = models.FloatField(blank=True, null=True)
    building_material_txt = models.CharField(max_length=250, blank=True, null=True)
    housing_space = models.FloatField(blank=True, null=True)
    housing_stay_type = models.FloatField(blank=True, null=True)
    housing_stay_type_txt = models.CharField(max_length=250, blank=True, null=True)
    bed_room_count = models.FloatField(blank=True, null=True)
    other_room_count = models.FloatField(blank=True, null=True)
    kitchen_count = models.FloatField(blank=True, null=True)
    bath_room_count = models.FloatField(blank=True, null=True)
    holding_type = models.FloatField(blank=True, null=True)
    holding_type_txt = models.CharField(max_length=250, blank=True, null=True)
    electric_sources = models.FloatField(blank=True, null=True)
    electric_sources_txt = models.CharField(max_length=250, blank=True, null=True)
    water_sources = models.FloatField(blank=True, null=True)
    water_sources_txt = models.CharField(max_length=250, blank=True, null=True)
    sewage = models.FloatField(blank=True, null=True)
    sewage_txt = models.CharField(max_length=250, blank=True, null=True)
    mobile_count = models.FloatField(blank=True, null=True)
    telephone_count = models.FloatField(blank=True, null=True)
    internet_users_count = models.FloatField(blank=True, null=True)
    internet_connection = models.FloatField(blank=True, null=True)
    car_count = models.FloatField(blank=True, null=True)
    tv_count = models.FloatField(blank=True, null=True)
    income_avg = models.FloatField(blank=True, null=True)
    housing_act_economic = models.FloatField(blank=True, null=True)
    death_status = models.FloatField(blank=True, null=True)
    member_name = models.CharField(max_length=250, blank=True, null=True)
    id_number_member = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    nationality = models.FloatField(blank=True, null=True)
    mobile = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    insert_by = models.FloatField(blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    update_by = models.FloatField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fcp_family_tab'


class GenErrorTab(models.Model):
    error_id = models.FloatField(primary_key=True)
    rp = models.ForeignKey('GenResearchPeriodTab', models.DO_NOTHING, blank=True, null=True)
    error_code = models.CharField(max_length=500, blank=True, null=True)
    error_type = models.NullBooleanField()
    part_error = models.FloatField(blank=True, null=True)
    table_name = models.CharField(max_length=3000, blank=True, null=True)
    tablet_condition = models.CharField(max_length=3000, blank=True, null=True)
    desktop_condition = models.CharField(max_length=3000, blank=True, null=True)
    message = models.CharField(max_length=3000, blank=True, null=True)
    message2 = models.CharField(max_length=3000, blank=True, null=True)
    on_off_tablet = models.NullBooleanField()
    on_off_desktop = models.NullBooleanField()
    colume_related = models.CharField(max_length=200, blank=True, null=True)
    colume_related2 = models.CharField(max_length=200, blank=True, null=True)
    colume_related3 = models.CharField(max_length=200, blank=True, null=True)
    error_sort = models.FloatField(blank=True, null=True)
    level_flag = models.NullBooleanField()
    rule_desc = models.CharField(max_length=3000, blank=True, null=True)
    col1 = models.CharField(max_length=1000, blank=True, null=True)
    col2 = models.CharField(max_length=1000, blank=True, null=True)
    col3 = models.CharField(max_length=1000, blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)
    error_apply_id = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gen_error_tab'


class GenSampleTab(models.Model):
    sample_id = models.FloatField(primary_key=True)
    family_id = models.FloatField(blank=True, null=True)
    rp = models.ForeignKey('GenResearchPeriodTab', models.DO_NOTHING, blank=True, null=True)
    w_a = models.ForeignKey('GenWorkAreaInfTab', models.DO_NOTHING, blank=True, null=True)
    census_area = models.CharField(max_length=200, blank=True, null=True)
    family_no = models.FloatField(blank=True, null=True)
    place = models.ForeignKey('GenPlacesViewTab', models.DO_NOTHING, blank=True, null=True)
    check_dig = models.FloatField(blank=True, null=True)
    hara = models.FloatField(blank=True, null=True)
    section_no = models.FloatField(blank=True, null=True)
    block_no = models.FloatField(blank=True, null=True)
    build_no = models.FloatField(blank=True, null=True)
    unit_no = models.FloatField(blank=True, null=True)
    sample_month = models.IntegerField(blank=True, null=True)
    stratumno = models.CharField(max_length=200, blank=True, null=True)
    hara_aname = models.CharField(max_length=100, blank=True, null=True)
    head_family = models.CharField(max_length=255, blank=True, null=True)
    sample_member_tot = models.CharField(max_length=255, blank=True, null=True)
    lat_y = models.FloatField(blank=True, null=True)
    lng_x = models.FloatField(blank=True, null=True)
    sample_status = models.FloatField(blank=True, null=True)
    sample_use_status = models.FloatField(blank=True, null=True)
    data_giver_name = models.CharField(max_length=250, blank=True, null=True)
    data_giver_phone = models.CharField(max_length=250, blank=True, null=True)
    data_giver_email = models.CharField(max_length=250, blank=True, null=True)
    visit_status = models.FloatField(blank=True, null=True)
    visit_status_txt = models.CharField(max_length=250, blank=True, null=True)
    lat_y_new = models.FloatField(blank=True, null=True)
    lng_x_new = models.FloatField(blank=True, null=True)
    no_of_member = models.FloatField(blank=True, null=True)
    t_start_date = models.DateField(blank=True, null=True)
    t_end_date = models.DateField(blank=True, null=True)
    t_update_date = models.DateField(blank=True, null=True)
    family_status = models.FloatField(blank=True, null=True)
    family_locked = models.FloatField(blank=True, null=True)
    desktop_error_status = models.IntegerField(blank=True, null=True)
    desktop_warning_status = models.IntegerField(blank=True, null=True)
    sms_flag = models.NullBooleanField()
    insert_by = models.FloatField(blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    update_by = models.FloatField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)
    contact_status = models.NullBooleanField()
    place_id_temp = models.FloatField(blank=True, null=True)
    place_id_temp_2 = models.FloatField(blank=True, null=True)
    family_phone_no = models.FloatField(blank=True, null=True)
    sample_member_name = models.CharField(max_length=350, blank=True, null=True)
    building_type_id = models.FloatField(blank=True, null=True)
    unit_type_id = models.FloatField(blank=True, null=True)
    family_nat_id = models.FloatField(blank=True, null=True)
    weight_1 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gen_sample_tab'
        unique_together = (('rp', 'census_area', 'family_no', 'sample_month'),)


class GenWorkAreaInfTab(models.Model):
    w_a_id = models.FloatField(primary_key=True)
    rp_id = models.FloatField(blank=True, null=True)
    supervisor = models.IntegerField(blank=True, null=True)
    vice = models.FloatField(blank=True, null=True)
    associate = models.IntegerField(blank=True, null=True)
    inspector = models.IntegerField(blank=True, null=True)
    controller = models.IntegerField(blank=True, null=True)
    researcher = models.IntegerField(blank=True, null=True)
    w_a_type = models.ForeignKey('GenWorkTypeTab', models.DO_NOTHING, blank=True, null=True)
    status = models.FloatField(blank=True, null=True)
    insert_by = models.FloatField(blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    update_by = models.FloatField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gen_work_area_inf_tab'
        unique_together = (('rp_id', 'supervisor', 'vice', 'associate', 'inspector', 'controller', 'researcher'),)


class GenPlacesViewTab(models.Model):
    admin = models.IntegerField()
    admin_name = models.CharField(max_length=50)
    region_id = models.FloatField(blank=True, null=True)
    region = models.FloatField(blank=True, null=True)
    region_name = models.CharField(max_length=50, blank=True, null=True)
    region_name_eng = models.CharField(max_length=100, blank=True, null=True)
    center_id = models.FloatField(blank=True, null=True)
    center = models.FloatField()
    center_name = models.CharField(max_length=50, blank=True, null=True)
    center_mgr_name = models.CharField(max_length=300, blank=True, null=True)
    center_mgr_phone = models.BigIntegerField(blank=True, null=True)
    general_notes = models.CharField(max_length=500, blank=True, null=True)
    gps_let = models.CharField(max_length=100, blank=True, null=True)
    gps_lng = models.CharField(max_length=100, blank=True, null=True)
    inspector_notes = models.CharField(max_length=500, blank=True, null=True)
    revision_status = models.NullBooleanField()
    place_id = models.FloatField(primary_key=True)
    city = models.IntegerField(blank=True, null=True)
    place_name = models.CharField(max_length=100, blank=True, null=True)
    sup_city = models.IntegerField(blank=True, null=True)
    sup_city_name = models.CharField(max_length=100, blank=True, null=True)
    place_type = models.FloatField(blank=True, null=True)
    place_location = models.CharField(max_length=80, blank=True, null=True)
    road_type = models.FloatField(blank=True, null=True)
    dir_type = models.FloatField(blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    n_degree = models.IntegerField(blank=True, null=True)
    n_minute = models.IntegerField(blank=True, null=True)
    n_second = models.IntegerField(blank=True, null=True)
    e_degree = models.IntegerField(blank=True, null=True)
    e_minute = models.IntegerField(blank=True, null=True)
    e_second = models.IntegerField(blank=True, null=True)
    place_max = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gen_places_view_tab'


class GenResearchPeriodTab(models.Model):
    rp_id = models.FloatField(primary_key=True)
    rp_name = models.CharField(max_length=600)
    rp_short_name = models.CharField(max_length=200, blank=True, null=True)
    rp_start_date = models.DateField(blank=True, null=True)
    rp_end_date = models.DateField(blank=True, null=True)
    rb_review_end_date = models.DateField(blank=True, null=True)
    mandate_date = models.DateField(blank=True, null=True)
    mandate_start_date = models.DateField(blank=True, null=True)
    mandate_end_date = models.DateField(blank=True, null=True)
    first_signature_name = models.CharField(max_length=300, blank=True, null=True)
    first_signature_job = models.CharField(max_length=300, blank=True, null=True)
    second_signature_name = models.CharField(max_length=300, blank=True, null=True)
    second_signature_job = models.CharField(max_length=300, blank=True, null=True)
    rp_status = models.FloatField()
    quiz_id = models.FloatField(blank=True, null=True)
    error_status = models.FloatField(blank=True, null=True)
    error_last_date = models.DateField(blank=True, null=True)
    count_census_area = models.FloatField(blank=True, null=True)
    count_family = models.FloatField(blank=True, null=True)
    nationality_cat = models.FloatField(blank=True, null=True)
    sample_status = models.FloatField(blank=True, null=True)
    sample_sys_status = models.FloatField(blank=True, null=True)
    survey_type = models.FloatField(blank=True, null=True)
    bi_data_status = models.FloatField(blank=True, null=True)
    member_table_name = models.CharField(max_length=350, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gen_research_period_tab'


class GenWorkTypeTab(models.Model):
    work_type_id = models.FloatField(primary_key=True)
    work_type_desc = models.CharField(max_length=1000)
    seq_no = models.FloatField()
    active_flag = models.FloatField()
    ref_work_type_id = models.FloatField(blank=True, null=True)
    multi_admin_status = models.NullBooleanField()
    main_w_a_status = models.NullBooleanField()
    cand_status = models.FloatField(blank=True, null=True)
    ecproj_work_type_id = models.CharField(max_length=5, blank=True, null=True)
    group_support = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gen_work_type_tab'
