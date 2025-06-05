import { Card, Typography } from "antd";
import type { IItem } from "../../types/types";

const { Title, Text } = Typography;

interface CatalogItemCardProps {
    item: IItem;
}

const CatalogItemCard: React.FC<CatalogItemCardProps> = ({ item }) => {
    return (
        <Card style={{
            backgroundColor: '#fafafa',
            borderLeft: '4px solid #1890ff',
            width: '100%'
        }}>
            <Title level={4}>{item.name}</Title>
            <Text>{item.description}</Text>
        </Card>
    );
}

export default CatalogItemCard;