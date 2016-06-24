function subject_session = get_multipie_subject_session_expr(filepath)

n2r=@num2str;

mpie_parts=get_multipie_parts_from_filename(filepath);

subject_session = [n2r(kv_get('subject',mpie_parts)) '_' n2r(kv_get('session',mpie_parts)) '_' n2r(kv_get('expression',mpie_parts))];