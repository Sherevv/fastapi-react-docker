import { useShow, useOne, IResourceComponentsProps } from "@pankod/refine-core";
import { Show, Typography, Tag, RefreshButton } from "@pankod/refine-antd";

import { IBroker } from "interfaces";
import { useParams } from "react-router-dom";

const { Title, Text } = Typography;

export const BrokerShow: React.FC<IResourceComponentsProps> = () => {
    //const { action, id } = useParams();
    const { queryResult } = useShow<IBroker>({
        //id: id,
        metaData:{
                fields: [
                    "id",
                    "name",
                ],
            },
        }
    );
    const { data, isLoading } = queryResult;
    const record = data?.data;

    return (
        <Show isLoading={isLoading}
              pageHeaderProps={{ extra: <RefreshButton onClick={() => queryResult.refetch()} /> }}>
            <Title level={5}>Id</Title>
            <Text>{record?.id}</Text>

            <Title level={5}>Name</Title>
            <Text>{record?.name}</Text>
        </Show>
    );
};