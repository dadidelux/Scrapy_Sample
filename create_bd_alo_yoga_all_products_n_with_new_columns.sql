
CREATE TABLE IF NOT EXISTS default.bd_alo_yoga_all_products_n (
    `gid` String,
    `handle` Nullable(String),
    `minPrice` Nullable(String),
    `maxPrice` Nullable(String),
    `onlineStoreUrl` Nullable(String),
    `productType` Nullable(String),
    `images` Nullable(String),
    `processed_date` Nullable(String),
    `tag_Men's Content` Nullable(String),
    tag_YGroup_M1224R Nullable(String),
    `tag_EcomVideo-Ikce` Nullable(String),
    tag_MensUnisexPixlee Nullable(String),
    tag_YGroup_MensW3550RG Nullable(String),
    `tag_SU25MD1-family` Nullable(String),
    `tag_EcomVideo-Shomari` Nullable(String),
    tag_YGroup_M6123R Nullable(String),
    `tag_FA24MD1-family` Nullable(String),
    `tag_HO22MMidnightGreen-family` Nullable(String),
    tag_YGroup_M1205R Nullable(String),
    `tag_SU22MRust-family` Nullable(String),
    tag_YGroup_MensU3041RG Nullable(String),
    tag_YGroup_MensU5013RG Nullable(String),
    tag_YGroup_M6154R Nullable(String),
    `tag_EcomVideo-Dale` Nullable(String)
) ENGINE = MergeTree()
ORDER BY gid;
