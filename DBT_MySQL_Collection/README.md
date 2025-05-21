


1. Install dbt mysql
pip install dbt-mysql

Có 1 điều rất vớ vẩn là cài dbt-mysql thì khỏi dùng dbt-bigquery vì khi cài dbt-mysql thì bản dbt bị downgrade xuống 1.7 trong khi dbt-bigquery lại yêu cầu version là 1.9. Hi Vọng vấn đề này sẽ sớm dc pipy giải quyết.

2. Init project 
dbt init DBT_MySQL_Collection


3. update content file 
./dbt_project.yml
./profiles.yml

4. dun "dbt debug" for testing config & connection

# Hackerrank Challenges
- create database hackerrank manually
1. occupations
Steps:
    - create table occupations trong databbase hackkerrank
        Nhưng có vẻ DBT không tạo được table bên ngoài database/schema đã được khai báo trong file profiles.yml
        Nên chắc phải tạo table và insert data bằng tay



# Issues
1. No database selected
khi select cần thêm tên DB vào trước table. ví dụ hackerank.occupations
2. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 18
F: Trong dbt .sql files, bạn không cần dùng ; ở cuối dòng SELECT, nếu có ; đôi khi gây lỗi compile.

# References
