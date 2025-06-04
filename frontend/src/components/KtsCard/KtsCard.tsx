import { Card, Typography } from "antd";
import type { IKts } from "../../types/types";
import UnitCardsList from "../UnitCardsList/UnitCardsList";
const { Text, Title } = Typography;

interface KtsCardProps {
    kts: IKts;
}
const KtsCard: React.FC<KtsCardProps> = ({ kts }) => {

    return (
        <Card
            title={
                <>
                    <Title level={2}>{kts.name}</Title>
                    <Text>{kts.description}</Text>
                </>
            }
            style={{
                width: '100%',
                marginBottom: 16,
                backgroundColor: '#fafafa',
                borderLeft: '4px solid #faad14',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
            }}
        >
            <UnitCardsList units_list={kts.units_list ?? []}/>
        </Card>
    )

}

export default KtsCard;