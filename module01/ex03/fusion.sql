
BEGIN;

-- 1. Supprimer l'ancienne table si elle existe
DROP TABLE IF EXISTS item_nodup;

-- 2. Créer une table avec un seul enregistrement par produit
CREATE TABLE item_nodup AS
SELECT
    product_id,
    MAX(category_id) AS category_id,
    MAX(category_code) AS category_code,
    MAX(brand) AS brand
FROM item
GROUP BY product_id;

-- 3. Ajouter les colonnes à customers si nécessaire
ALTER TABLE customers_clean
    ADD COLUMN IF NOT EXISTS category_id BIGINT,
    ADD COLUMN IF NOT EXISTS category_code VARCHAR(255),
    ADD COLUMN IF NOT EXISTS brand VARCHAR(255);

-- 4. Mettre à jour les lignes existantes de customers
UPDATE customers_clean AS c
SET
    category_id = i.category_id,
    category_code = i.category_code,
    brand = i.brand
FROM item_nodup AS i
WHERE c.product_id = i.product_id;

COMMIT;
