import React from 'react';
import { Typography } from 'antd';
import type { IItem } from '../../types/types';
import ItemCard from '../ItemCard/ItemCard';

const { Text } = Typography;

interface ItemCardProps {
    items_list: IItem[];
}

const ItemCardsList: React.FC<ItemCardProps> = ({ items_list }) => {
    return (
        <>
            {(!items_list.length || !items_list) ? (
                <Text>Items нет</Text>
            ) : (
                items_list.map((item) =>
                    <ItemCard key={item.id} item={item} />
                )
            )}
        </>
    );
};

export default ItemCardsList;
