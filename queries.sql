SELECT "blogapp_article"."id",
"blogapp_article"."title",
"blogapp_article"."pub_date",
"blogapp_article"."author_id",
"blogapp_article"."category_id",
"blogapp_category"."id",
"blogapp_category"."name"
FROM "blogapp_article"
INNER JOIN "blogapp_category"
ON ("blogapp_article"."category_id" = "blogapp_category"."id");



