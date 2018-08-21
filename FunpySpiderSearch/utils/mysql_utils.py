__author__ = 'mtianyan'
__date__ = '2018/8/20 08:51'

field_list = ['title', 'url', 'url_object_id', 'salary_min', 'salary_max', 'job_city',
              'work_years_min', 'work_years_max', 'degree_need''job_type', 'publish_time',
              'job_advantage', 'job_desc', 'job_addr', 'company_name', 'company_url',
              'tags', 'crawl_time']
duplicate_key_update = ['praise_nums', 'comment_nums', 'crawl_time', 'fav_nums']


def fun_sql_insert(field_list: list, duplicate_key_update: list, table_name: str):
    field_str = ""
    field_s = ""
    update_s = ""
    params_s = ""
    for field in field_list:
        field_str += field + ','
        field_s += '%s,'
        params_s += 'self["' + str(field) + '"],\n\t'
    for duplicate_key in duplicate_key_update:
        update_s += str(duplicate_key) + "=VALUES(" + str(duplicate_key) + '),'
    params_txt = "params = (\n" + params_s + ")"
    sql = "insert into {0}({1}) VALUES({2}) \n\t\t\t\t\t\t\t\t\t\tON DUPLICATE KEY UPDATE  {3}".format(table_name,
                                                                                                       field_str[:-1],
                                                                                                       field_s[:-1],
                                                                                                       update_s[:-1])
    print(sql)
    return sql, params_txt


if __name__ == '__main__':
    print(fun_sql_insert(field_list, duplicate_key_update, "jobbole_article"))
