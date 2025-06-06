import { Button, Typography } from "antd";
import { useGetCatalogKtsQuery } from "../../redux/services/catalogApi";
import Loader from "../../components/Loader/Loader";
import KtsCardsList from "../../components/KtsCardsList/KtsCardsList";
import { PlusOutlined } from '@ant-design/icons';
import AddKtsModal from "../../components/AddKtsModal/AddKtsModal";
import { useState } from "react";

const { Title } = Typography;

const CatalogKtsPage: React.FC = () => {

    const { data: kts_list, isLoading, isError } = useGetCatalogKtsQuery();
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    return (
        <>
            <div style={{ display: 'flex', gap: 16, alignItems: 'center', marginBottom: 16 }}>
                <Title style={{ margin: 0 }}>Каталог KTC</Title>
                <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={() => setIsModalOpen(true)}
                />
            </div>

            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <KtsCardsList kts_list={kts_list ?? []} />
            )}

            <AddKtsModal
                isModalOpen={isModalOpen}
                onCancel={() => setIsModalOpen(false)}
            />
        </>
    );
}

export default CatalogKtsPage;