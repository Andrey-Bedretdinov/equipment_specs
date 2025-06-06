import { Card, Typography } from "antd";
import type { IKts } from "../../types/types";

const { Title, Text } = Typography;

interface CatalogKtsCardProps {
    kts: IKts;
}

const CatalogKtsCard: React.FC<CatalogKtsCardProps> = ({ kts }) => {
    return (
        <Card style={{
            backgroundColor: '#fafafa',
            borderLeft: '4px solid #faad14',
            width: '100%'
        }}>
            <Title level={4}>{kts.name}</Title>
            <Text>{kts.description}</Text>
        </Card>
    );
}

export default CatalogKtsCard;