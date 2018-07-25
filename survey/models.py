from django.db import models

# Create your models here.


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
    rp_id = models.FloatField(blank=True, null=True)
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
