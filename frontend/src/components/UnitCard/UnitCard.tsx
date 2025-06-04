import { Button, Card, Typography } from "antd";
import { DownOutlined, RightOutlined } from '@ant-design/icons';
import type { IUnit } from "../../types/types";
import ItemCardsList from "../ItemCardsList/ItemCardsList";
import { useState } from "react";
const { Text, Title } = Typography;

interface UnitCardProps {
    unit: IUnit;
}
const UnitCard: React.FC<UnitCardProps> = ({ unit }) => {

    const [collapsed, setCollapsed] = useState<boolean>(true);

    const toggleCollapse = () => {
        setCollapsed(prev => !prev);
    };

    return (
        <Card
            title={
                <div
                    style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                    <Button
                        type="text"
                        icon={collapsed ? <RightOutlined /> : <DownOutlined />}
                        onClick={toggleCollapse}
                    />
                    <div>
                        <Title level={3}>{unit.name}</Title>
                        <Text>{unit.name}</Text><br/>
                        <Text strong>Итоговая стоимость: {unit.price} RUB</Text>
                    </div>
                </div>
            }
            style={{
                width: '100%',
                marginBottom: 16,
                backgroundColor: '#fafafa',
                borderLeft: '4px solid #52c41a',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
            }}
        >
            {!collapsed && <ItemCardsList items_list={unit.items_list ?? []} />}
        </Card>
    )

}

export default UnitCard;