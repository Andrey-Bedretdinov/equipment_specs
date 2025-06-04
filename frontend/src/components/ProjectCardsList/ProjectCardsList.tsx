import { Button, Result, Spin, Typography } from "antd";
import { useGetProjectsQuery } from "../../redux/services/projectsApi"
import ProjectCard from "../ProjectCard/ProjectCard";

const { Title } = Typography;

const ProjectCardsList = () => {

    const { data, isLoading, isError } = useGetProjectsQuery();

    return (
        <>
            <Title level={2} >Список проектов</Title>

            {isLoading && (
                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    minHeight: '50vh',
                }}>
                    <Spin size="large" />
                </div>
            )}

            {isError && (
                <Result
                    status="error"
                    title="Произошла ошибка"
                    subTitle="Не удалось загрузить список проектов. Попробуйте позже."
                    extra={[
                        <Button type="primary" onClick={() => window.location.reload()}>
                            Обновить
                        </Button>,
                    ]}
                />
            )}

            {data?.map((project) =>
                <ProjectCard key={project.id} project={project} />
            )}
        </>
    )
}

export default ProjectCardsList;