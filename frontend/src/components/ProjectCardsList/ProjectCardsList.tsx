import { Button, Typography } from "antd";
import { useGetProjectsQuery } from "../../redux/services/projectsApi"
import ProjectCard from "../ProjectCard/ProjectCard";
import Loader from "../Loader/Loader";
import { useState } from "react";
import AddProjectModal from "../AddProjectModal/AddProjectModal";

const { Title } = Typography;

const ProjectCardsList = () => {

    const { data, isLoading, isError } = useGetProjectsQuery();
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    return (
        <div style={{display: 'flex', flexDirection:'column', gap: 16}}>
            <div style={{display: 'flex', alignItems:'center', justifyContent: 'space-between'}}>
                <Title level={2} >Список проектов</Title>
                <Button 
                    type='primary'
                    onClick={() => setIsModalOpen(true)}
                >
                    Добавить проект</Button>
            </div>

            <Loader isLoading={isLoading} isError={isError} />

            {data?.map((project) =>
                <ProjectCard key={project.id} project={project} />
            )}

            <AddProjectModal
                isModalOpen={isModalOpen}
                onCancel={() => setIsModalOpen(false)}
            />
        </div>
    )
}

export default ProjectCardsList;