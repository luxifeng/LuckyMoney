-- 个股列表
DROP TABLE IF EXISTS stock_basic;
CREATE TABLE stock_basic(
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '自增id',
    ts_code VARCHAR(24) NOT NULL UNIQUE DEFAULT '000000' COMMENT 'TS代码',
    symbol VARCHAR(24) NOT NULL UNIQUE DEFAULT '000000' COMMENT '股票代码',
    name VARCHAR(128) COMMENT '股票名称',
    area VARCHAR(24) COMMENT '所在地域',
    industry VARCHAR(24) COMMENT '所属行业',
    fullname VARCHAR(128) COMMENT '股票全称',
    enname VARCHAR(128) COMMENT '英文全称',
    market VARCHAR(24) COMMENT '市场类型',
    exchange VARCHAR(24) COMMENT '交易所代码',
    curr_type VARCHAR(24) COMMENT '交易货币',
    list_status TINYINT COMMENT '上市状态：0上市 1退市 2暂停上市',
    list_date DATE COMMENT '上市日期',
    delist_date DATE COMMENT '退市日期',
    is_hs TINYINT COMMENT '是否沪深港通标的，0否 1沪股通 2深股通'
);

-- 个股行情+指标
DROP TABLE IF EXISTS stock_price
CREATE TABLE stock_price (
    id INT AUTO_INCREMENT COMMENT '自增id',
    ts_code VARCHAR(24) NOT NULL DEFAULT '000000' COMMENT '股票代码',
    trade_date DATE NOT NULL DEFAULT '1970-01-01' COMMENT '交易日期',
    trade_time TIME  COMMENT '交易时间',
    open DECIMAL(18, 4) NOT NULL COMMENT '开盘价',
    high DECIMAL(18, 4) NOT NULL COMMENT '最高价',
    low DECIMAL(18, 4) NOT NULL COMMENT '最低价',
    close DECIMAL(18, 4) NOT NULL COMMENT '收盘价',
    vol BIGINT COMMENT '成交量',
    amount NUMERIC(10) COMMENT '成交额',
    pe NUMERIC(10) COMMENT '市盈率',
    pe_ttm NUMERIC(10) COMMENT 'tushare滚动市盈率',
    pe_ttm_my NUMERIC(10) COMMENT '我的滚动市盈率',
    pb NUMERIC(10) COMMENT '市净率',
    total_share NUMERIC(10) COMMENT '总股本(万)',
    float_share NUMERIC(10) COMMENT '流通股本(万)',
    total_mv NUMERIC(10) COMMENT '总市值(万)',
    circ_mv NUMERIC(10) COMMENT '流通市值(万)',
    PRIMARY KEY (id),
    CONSTRAINT stock_trade UNIQUE (ts_code,trade_date)
) PARTITION BY RANGE(YEAR(trade_date))(
    PARTITION p0 VALUES LESS THAN (2006),
    PARTITION p0 VALUES LESS THAN (2011),
    PARTITION p0 VALUES LESS THAN (2016),
    PARTITION p0 VALUES LESS THAN (2021),
    PARTITION p0 VALUES LESS THAN (2026),
    PARTITION p0 VALUES LESS THAN MAXVALUE
);

-- 个股利润表

-- 指数列表
DROP TABLE IF EXISTS index_basic
CREATE TABLE index_basic(
    id INT AUTO_INCREMENT COMMENT '自增id',
    ts_code VARCHAR(24) NOT NULL UNIQUE DEFAULT '000000' COMMENT 'TS代码',
    name VARCHAR(24) COMMENT '简称',
    fullname VARCHAR(24) COMMENT '指数全称',
    market VARCHAR(24) COMMENT '市场',
    publisher VARCHAR(24) COMMENT '发布方',
    index_type VARCHAR(24) COMMENT '指数风格',
    category VARCHAR(24) COMMENT '指数类别',
    base_date VARCHAR(24) COMMENT '基期',
    base_point NUMERIC(24) COMMENT '基点',
    list_date VARCHAR(24) COMMENT '发布日期',
    weight_rule VARCHAR(24) COMMENT '加权方式',
    desc VARCHAR(24) COMMENT '描述',
    exp_date VARCHAR(24) COMMENT '终止日期',
    PRIMARY KEY (id)
)

-- 指数成分与权重表
DROP TABLE IF EXISTS index_comp
CREATE TABLE index_comp(
    id INT AUTO_INCREMENT COMMENT '自增id',
    index_code VARCHAR(24) NOT NULL DEFAULT '000000' COMMENT '指数代码',
    con_code VARCHAR(24) COMMENT '成分代码',
    trade_date DATE NOT NULL DEFAULT '1970-01-01' COMMENT '交易日期',
    weight NUMERIC(10) COMMENT '权重',
    PRIMARY KEY (id)
) PARTITION BY RANGE(YEAR(trade_date))(
    PARTITION p0 VALUES LESS THAN (2006),
    PARTITION p0 VALUES LESS THAN (2011),
    PARTITION p0 VALUES LESS THAN (2016),
    PARTITION p0 VALUES LESS THAN (2021),
    PARTITION p0 VALUES LESS THAN (2026),
    PARTITION p0 VALUES LESS THAN MAXVALUE
);

-- 指数pe
DROP TABLE IF EXISTS index_pe
CREATE TABLE index_pe (
    id INT AUTO_INCREMENT COMMENT '自增id',
    index_code VARCHAR(24) NOT NULL DEFAULT '000000' COMMENT '指数代码',
    trade_date DATE NOT NULL DEFAULT '1970-01-01' COMMENT '交易日期',
    pe_ttm
)