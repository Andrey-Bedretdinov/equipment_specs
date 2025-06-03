import { Card, Typography } from 'antd';
import type { ItemNode } from "../../types/types";
import styles from './ItemCard.module.css';

const { Text } = Typography;

const ItemCard: React.FC<{ item: ItemNode }> = ({ item }) => (
    <Card size="small" className={styles.card}>
        <Text strong>{item.name}</Text> — <Text>{item.description}</Text>
        <div><Text type="secondary">Каталог:</Text> {item.catalog_code}</div>
        <div><Text type="secondary">Поставщик:</Text> {item.supplier}</div>
        <div><Text type="secondary">Цена:</Text> {item.price} {item.currency}</div>
        <div><Text type="secondary">Производитель:</Text> {item.manufacturer}</div>
        <div><Text type="secondary">Доставка:</Text> {item.deliveryType}</div>
        <div><Text type="secondary">Количество:</Text> {item.quantity}</div>
    </Card>
);

export default ItemCard;
