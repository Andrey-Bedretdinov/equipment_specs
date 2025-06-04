import React from 'react';
import { Card, Descriptions, Typography } from 'antd';
import type { IItem } from '../../types/types';

const { Text } = Typography;

interface ItemCardProps {
  item: IItem;
}

const ItemCard: React.FC<ItemCardProps> = ({ item }) => {
  return (
    <Card
      title={<Text strong>{item.name}</Text>}
      style={{
        width: '100%',
        marginBottom: 16,
        backgroundColor: '#fafafa',
        borderLeft: '4px solid #1890ff',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
      }}
    >
      <Descriptions size="small" column={1}>
        <Descriptions.Item label="Описание">
          {item.description}
        </Descriptions.Item>
        <Descriptions.Item label="Цена">
          {item.price} {item.currency}
        </Descriptions.Item>
        <Descriptions.Item label="Поставщик">
          {item.supplier}
        </Descriptions.Item>
        <Descriptions.Item label="Код в каталоге">
          {item.catalog_code}
        </Descriptions.Item>
        <Descriptions.Item label="Производство">
          {item.manufactured}
        </Descriptions.Item>
        <Descriptions.Item label="Тип поставки">
          {item.delivery_type}
        </Descriptions.Item>
        <Descriptions.Item label="Количество">
          {item.quantity}
        </Descriptions.Item>
      </Descriptions>
    </Card>
  );
};

export default ItemCard;
