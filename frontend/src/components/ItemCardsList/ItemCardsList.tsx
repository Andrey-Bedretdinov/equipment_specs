import React from 'react';
import type { IItem } from '../../types/types';
import ItemCard from '../ItemCard/ItemCard';

interface ItemCardProps {
    items_list: IItem[];
    canDelete?: boolean;
}

const ItemCardsList: React.FC<ItemCardProps> = ({ items_list, canDelete }) => {
    return (
        <>
            { items_list.map((item) =>
                    <ItemCard canDelete={canDelete} key={item.id} item={item} />
            )}
        </>
    );
};

export default ItemCardsList;
