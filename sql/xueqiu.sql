DROP TABLE IF EXISTS xueqiu_users;
CREATE TABLE xueqiu_users (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id varchar(64) NOT NULL COMMENT '用户id',
  description varchar(4096) NOT NULL COMMENT '描述签名',
  screen_name varchar(128) DEFAULT NULL COMMENT '用户名',
  friends_count int(11) DEFAULT NULL COMMENT '关注人数',
  followers_count int(11) DEFAULT NULL COMMENT '粉丝人数',
  province varchar(64) DEFAULT NULL COMMENT '省份',
  city varchar(64) DEFAULT NULL COMMENT '城市',
  gender varchar(64) DEFAULT NULL COMMENT '性别',
  profile varchar(512) DEFAULT NULL COMMENT '账户',
  update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '插入时间戳',
  UNIQUE KEY (user_id),
  KEY id (id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS xueqiu_zuhe;
CREATE TABLE xueqiu_zuhe (
  f_id int(11) NOT NULL AUTO_INCREMENT,
  f_title varchar(64) NOT NULL COMMENT '策略名称',
  f_sign varchar(64) DEFAULT NULL COMMENT '策略标签',
  f_slogan varchar(128) DEFAULT NULL COMMENT '策略标语',
  f_detail varchar(512) DEFAULT NULL COMMENT '策略说明',
  f_updatetime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '插入时间戳',
  UNIQUE KEY (f_title),
  KEY f_id (f_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;