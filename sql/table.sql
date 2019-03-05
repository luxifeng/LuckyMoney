-- 个股列表

-- 个股信息表 = 行情+指标
DROP TABLE IF EXISTS stock
CREATE TABLE stock(
    id INT AUTO_INCREMENT COMMENT '自增id',
    ts_code VARCHAR(24) NOT NULL DEFAULT '000000' COMMENT '股票代码',
    trade_date DATE NOT NULL DEFAULT '1970-01-01' COMMENT '交易日期',
    open NUMERIC(10) COMMENT '开盘价',
    high NUMERIC(10) COMMENT '最高价',
    low NUMERIC(10) COMMENT '最低价',
    close NUMERIC(10) COMMENT '收盘价',
    pre_close NUMERIC(10) COMMENT '昨收价',
    change NUMERIC(10) COMMENT '涨跌额',
    pct_chg NUMERIC(10) COMMENT '涨跌幅',
    vol NUMERIC(10) COMMENT '成交量',
    amount NUMERIC(10) COMMENT '成交额',
    pe NUMERIC(10) COMMENT '市盈率',
    pe_ttm NUMERIC(10) COMMENT '滚动市盈率',
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

-- 指数列表

-- 指数成分与权重表
DROP TABLE IF EXISTS index_weight
CREATE TABLE index_weight(
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