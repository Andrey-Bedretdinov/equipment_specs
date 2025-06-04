import { Card, Typography } from "antd";
import type { IUnit } from "../../types/types";
const { Text, Title } = Typography;

interface UnitCardProps {
    unit: IUnit;
}
const UnitCard: React.FC<UnitCardProps> = ({ unit }) => {

    return (
        <Card
            title={
                <>
                    <Title level={3}>{unit.name}</Title>
                    <Text>{unit.description}</Text>
                </>
            }
            style={{
                width: '100%',
                marginBottom: 16,
                backgroundColor: '#fafafa',
                borderLeft: '4px solid #52c41a',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
            }}
        >

        </Card>
    )

}

export default UnitCard;