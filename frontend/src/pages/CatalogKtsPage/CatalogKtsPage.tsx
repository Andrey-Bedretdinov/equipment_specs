import { Button, Typography } from "antd";
import { useGetCatalogKtsQuery } from "../../redux/services/catalogApi";
import Loader from "../../components/Loader/Loader";
import KtsCardsList from "../../components/KtsCardsList/KtsCardsList";
import { PlusOutlined } from '@ant-design/icons';

const { Title } = Typography;

const CatalogKtsPage: React.FC = () => {

    const { data: kts_list, isLoading, isError } = useGetCatalogKtsQuery();

    return (
        <>
            <div style={{ display: 'flex', gap: 16, alignItems: 'center', marginBottom: 16 }}>
                <Title style={{ margin: 0 }}>Каталог KTC</Title>
                <Button
                    type="primary"
                    icon={<PlusOutlined />}
                />
            </div>

            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <KtsCardsList kts_list={kts_list ?? []} />
            )}
        </>
    );
}

export default CatalogKtsPage;