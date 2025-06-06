import React from "react";
import { Button, Card, Typography } from "antd";
import { DeleteOutlined } from '@ant-design/icons';
import type { IProject } from "../../types/types";
import { useNavigate } from "react-router-dom";
import { useDeleteProjectMutation } from "../../redux/services/projectsApi";

const { Text } = Typography

interface ProjectCardProps {
    project: IProject
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {

    const navigate = useNavigate();
    const [deleteProject] = useDeleteProjectMutation();

    const handleDelete = (event: React.MouseEvent<HTMLElement>) => {
        deleteProject(project.id)
        event.stopPropagation()
    }

    return (
        <Card
            hoverable
            onClick={() => navigate(`/projects/${project.id}`)}
            title={
                <div
                    style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                    }}>
                    <Text strong>{project.name}</Text>
                    <Button
                        type="primary"
                        danger
                        icon={<DeleteOutlined />}
                        onClick={(e) => handleDelete(e)}
                    />
                </div>
            }
        >
            <Text>{project.description}</Text>
        </Card>
    )
}

export default ProjectCard;