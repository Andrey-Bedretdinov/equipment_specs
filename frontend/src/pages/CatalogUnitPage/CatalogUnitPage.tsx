import { Button, Typography } from "antd";
import { useGetCatalogUnitsQuery } from "../../redux/services/catalogApi";
import { PlusOutlined } from '@ant-design/icons';
import Loader from "../../components/Loader/Loader";
import UnitCardsList from "../../components/UnitCardsList/UnitCardsList";
import { useState } from "react";
import AddUnitModal from "../../components/AddUnitModal/AddUnitModal";

const { Title } = Typography;

const CatalogUnitPage: React.FC = () => {

    const { data: units_list, isLoading, isError } = useGetCatalogUnitsQuery();
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    return (
        <>
            <div style={{ display: 'flex', gap: 16, alignItems: 'flex-end', marginBottom: 16 }}>
                <Title style={{ margin: 0 }}>Каталог Units</Title>
                <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={() => setIsModalOpen(true)}
                />
            </div>

            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <UnitCardsList units_list={units_list ?? []} />
            )}

            <AddUnitModal 
                isModalOpen={isModalOpen}
                onCancel={() => setIsModalOpen(false)}
            />

        </>
    );
}

export default CatalogUnitPage;