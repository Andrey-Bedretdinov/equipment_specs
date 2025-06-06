import { Card, Typography } from "antd";
import type { IUnit } from "../../types/types";

const { Title, Text } = Typography;

interface CatalogItemCardProps {
    unit: IUnit;
}

const CatalogUnitCard: React.FC<CatalogItemCardProps> = ({ unit }) => {
    return (
        <Card style={{
            backgroundColor: '#fafafa',
            borderLeft: '4px solid #52c41a',
            width: '100%'
        }}>
            <Title level={4}>{unit.name}</Title>
            <Text>{unit.description}</Text>
        </Card>
    );
}

export default CatalogUnitCard;