insert into users (email) values ('lrodriguez@4geeks.co');

insert into profiles (bio, github, users_id) values ('Profesor Programacion', 'ljavierrodriguez', 1);

insert into courses (name) values ('Aprender React');

insert into users_courses  (users_id, courses_id) values (1, 1);

insert into todos (label, done, users_id) values ('Aprender Python', false, 1);