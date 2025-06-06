import React, { useState } from 'react';
import { Button, Card, Descriptions, Typography } from 'antd';
import { DownOutlined, RightOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { IItem } from '../../types/types';
import { useLocation } from 'react-router-dom';

import styles from './ItemCard.module.css';


const { Text } = Typography;

interface ItemCardProps {
    item: IItem;
    canDelete?: boolean;
}

const ItemCard: React.FC<ItemCardProps> = ({ item, canDelete = true }) => {

    const [collapsed, setCollapsed] = useState<boolean>(true);

    const location = useLocation();
    const isProject = location.pathname.startsWith('/project');
    const isCatalogItemsPage = location.pathname.startsWith('/catalog/items');
    const isCatalogUnitsPage = location.pathname.startsWith('/catalog/units');
    const isCatalogKtsPage = location.pathname.startsWith('/catalog/kts');

    const toggleCollapse = () => {
        setCollapsed(prev => !prev);
    };

    const handleDelete = () => {
        if (isCatalogItemsPage) console.log('Удаление Итема из каталога итемов')
        else if (isCatalogUnitsPage) console.log('Удаление Итема из каталога юнитов')
        else if (isCatalogKtsPage) console.log('Уделение Итема из каталога ктс')
        else if (isProject) console.log('Удаление Итема из проекта')
    }

    return (
        <Card
            title={
                <div className={styles.cardTitle}>
                    <Button
                        type="text"
                        icon={collapsed ? <RightOutlined /> : <DownOutlined />}
                        onClick={toggleCollapse}
                    />
                    <div className={styles.cardDesc}>
                        <div>
                            <Text strong>{item.name}</Text><br />
                            <Text>{item.description}</Text>
                        </div>
                        <div className={styles.btnBox}>
                            {isCatalogItemsPage && (
                                <Button
                                    type="primary"
                                    icon={<EditOutlined />}
                                // onClick={() => setIsModalOpen(true)}
                                />
                            )}

                            {canDelete && (
                                <Button
                                    type="primary"
                                    danger
                                    icon={<DeleteOutlined />}
                                    onClick={handleDelete}
                                />
                            )}
                        </div>
                    </div>
                </div>
            }
            className={styles.card}
        >
            {!collapsed && (
                <Descriptions size="small" column={1}>
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
                    {item.quantity &&
                        <Descriptions.Item label="Количество">
                            {item.quantity}
                        </Descriptions.Item>}
                </Descriptions>
            )}
        </Card >
    );
};

export default ItemCard;
