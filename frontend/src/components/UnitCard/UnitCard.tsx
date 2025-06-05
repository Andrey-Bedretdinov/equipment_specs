import { Button, Card, Typography } from "antd";
import { DownOutlined, RightOutlined, EditOutlined } from '@ant-design/icons';
import type { IUnit } from "../../types/types";
import ItemCardsList from "../ItemCardsList/ItemCardsList";
import { useState } from "react";

import styles from './UnitCard.module.css';
import { useLocation } from "react-router-dom";
import AddItemToUnitModal from "../AddItemToUnitModal/AddItemToUnitModal";
const { Text, Title } = Typography;

interface UnitCardProps {
    unit: IUnit;
}
const UnitCard: React.FC<UnitCardProps> = ({ unit }) => {

    const [collapsed, setCollapsed] = useState<boolean>(true);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    const location = useLocation();
    const isEditable = location.pathname.startsWith('/catalog');

    const toggleCollapse = () => {
        setCollapsed(prev => !prev);
    };

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
                            <Title level={3}>{unit.name}</Title>
                            <Text>{unit.name}</Text><br />
                            <Text strong>Итоговая стоимость: {unit.price} RUB</Text>
                        </div>

                        {isEditable && (
                            <Button
                                type="primary"
                                icon={<EditOutlined />}
                                onClick={() => setIsModalOpen(true)}
                            />
                        )}
                    </div>
                </div>
            }
            className={styles.card}
        >
            {!collapsed && <ItemCardsList items_list={unit.items_list ?? []} />}

            {isModalOpen &&
                <AddItemToUnitModal
                    isModalOpen={isModalOpen}
                    onCancel={() => setIsModalOpen(false)}
                    unitId={unit.id}
                />}
        </Card>
    )

}

export default UnitCard;