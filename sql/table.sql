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
DROP TABLE IF EXISTS stock_price;
CREATE TABLE stock_price (
    ts_code VARCHAR(24) NOT NULL DEFAULT '000000' COMMENT '股票代码',
    trade_date DATE NOT NULL DEFAULT '1970-01-01' COMMENT '交易日期',
    trade_time TIME  COMMENT '交易时间',
    open DECIMAL(18, 4) NOT NULL COMMENT '开盘价',
    high DECIMAL(18, 4) NOT NULL COMMENT '最高价',
    low DECIMAL(18, 4) NOT NULL COMMENT '最低价',
    close DECIMAL(18, 4) NOT NULL COMMENT '收盘价',
    vol DECIMAL(18, 4) COMMENT '成交量',
    amount DECIMAL(18, 4) COMMENT '成交额',
    pe DECIMAL(18, 4) COMMENT '市盈率',
    pe_ttm DECIMAL(18, 4) COMMENT 'tushare滚动市盈率',
    pe_ttm_my DECIMAL(18, 4) COMMENT '我的滚动市盈率',
    pb DECIMAL(18, 4) COMMENT '市净率',
    total_share DECIMAL(18, 4) COMMENT '总股本(万)',
    float_share DECIMAL(18, 4) COMMENT '流通股本(万)',
    total_mv DECIMAL(18, 4) COMMENT '总市值(万)',
    circ_mv DECIMAL(18, 4) COMMENT '流通市值(万)',
    CONSTRAINT stock_trade UNIQUE (ts_code,trade_date)
) PARTITION BY RANGE(YEAR(trade_date))(
    PARTITION p0 VALUES LESS THAN (2006),
    PARTITION p1 VALUES LESS THAN (2011),
    PARTITION p2 VALUES LESS THAN (2016),
    PARTITION p3 VALUES LESS THAN (2021),
    PARTITION p4 VALUES LESS THAN (2026),
    PARTITION p5 VALUES LESS THAN MAXVALUE
);

-- 个股利润表
DROP TABLE IF EXISTS stock_profit;
CREATE TABLE stock_profit(
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增id',
    ts_code VARCHAR(24) NOT NULL DEFAULT '000000' COMMENT 'TS代码',
    ann_date DATE COMMENT '公告日期',
    f_ann_date DATE COMMENT '实际公告日期',
    end_date DATE COMMENT '报告期',
    report_type TINYINT COMMENT '报告类型',
    basic_eps DECIMAL(18, 4) COMMENT '基本每股收益',
    diluted_eps DECIMAL(18, 4) COMMENT '稀释每股收益',
    total_revenue DECIMAL(18, 4) COMMENT '营业总收入 (元，下同)',
    operate_profit DECIMAL(18, 4) COMMENT '营业利润',
    total_profit DECIMAL(18, 4) COMMENT '利润总额',
    income_tax DECIMAL(18, 4) COMMENT '所得税费用',
    n_income DECIMAL(18, 4) COMMENT '净利润(含少数股东损益)',
    n_income_attr_p DECIMAL(18, 4) COMMENT '净利润(不含少数股东损益)'
);

-- 指数列表
DROP TABLE IF EXISTS index_basic;
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
DROP TABLE IF EXISTS index_comp;
CREATE TABLE index_comp(
    index_code VARCHAR(24) NOT NULL DEFAULT '000000' COMMENT '指数代码',
    con_code VARCHAR(24) COMMENT '成分代码',
    trade_date DATE NOT NULL DEFAULT '1970-01-01' COMMENT '交易日期',
    weight NUMERIC(10) COMMENT '权重'
) PARTITION BY RANGE(YEAR(trade_date))(
    PARTITION p0 VALUES LESS THAN (2006),
    PARTITION p0 VALUES LESS THAN (2011),
    PARTITION p0 VALUES LESS THAN (2016),
    PARTITION p0 VALUES LESS THAN (2021),
    PARTITION p0 VALUES LESS THAN (2026),
    PARTITION p0 VALUES LESS THAN MAXVALUE
);

-- 指数pe
DROP TABLE IF EXISTS index_pe;
CREATE TABLE index_pe (
    id INT AUTO_INCREMENT COMMENT '自增id',
    index_code VARCHAR(24) NOT NULL DEFAULT '000000' COMMENT '指数代码',
    trade_date DATE NOT NULL DEFAULT '1970-01-01' COMMENT '交易日期',
    pe_ttm DECIMAL(18, 4) COMMENT '指数pe-ttm'
)