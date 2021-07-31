use db_shubham;

delimiter $$

drop trigger if exists t1 $$
create trigger t1 before insert on bmi for each row
begin
	if new.age is null or new.age < 1 then
		signal SQLSTATE '12345' set message_text = "age shud be not < 1";
	end if;
	if new.name is null or length(new.name) <= 1 then
		signal SQLSTATE '23456' set message_text = "invalid name";
	end if;
	if new.phone is null or length(new.phone) != 10 then
		signal SQLSTATE '34567' set message_text = "plz enter 10 digit phone no";
	end if;
end $$

delimiter ;
 