import { useParams } from "react-router-dom";
import { useGetProjectByIdQuery } from "../../redux/services/projectsApi";
import Loader from "../../components/Loader/Loader";
import ItemCardsList from "../../components/ItemCardsList/ItemCardsList";
import KtsCardsList from "../../components/KtsCardsList/KtsCardsList";
import { Button, Card, Typography } from "antd";
import { useState } from "react";
import AddElementsToProjectModal from "../../components/AddElementsToProjectModal/AddElementsToProjectModal";

const { Title, Text } = Typography;

const ProjectPage: React.FC = () => {
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    const { project_id } = useParams();
    const { data: project, isLoading, isError } = useGetProjectByIdQuery(project_id as string);

    return (
        <Card
            title={
                <>
                    <div
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between'
                        }}
                    >
                        <Title>{project?.name}</Title>
                        <Button 
                            type="primary"
                            onClick={() => setIsModalOpen(true)}
                        >Добавить элемент</Button>
                    </div>
                    <Text>{project?.description}</Text><br />
                    <Text strong>Итоговая стоимость: {project?.price} ₽</Text>
                </>
            }
        >


            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <>
                    <KtsCardsList kts_list={project?.kts_list ?? []} />
                    <ItemCardsList items_list={project?.items_list ?? []} />
                </>
            )}

            {isModalOpen && project && (
                <AddElementsToProjectModal
                    isModalOpen={isModalOpen}
                    onCancel={() => setIsModalOpen(false)}
                    projectId={project.id}
                />
            )}
        </Card>
    );
}

export default ProjectPage;