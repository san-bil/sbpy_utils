function out = multipie_camera_uid_to_class(uid)

map = multipie_camera_uid_to_class_mapping();

out=kvg(uid,map);