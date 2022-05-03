import { useShow, IResourceComponentsProps } from "@pankod/refine-core";
import { Show, Typography, RefreshButton } from "@pankod/refine-antd";

import { IBroker } from "interfaces";

const { Title, Text } = Typography;

export const BrokerShow: React.FC<IResourceComponentsProps> = () => {
    const { queryResult } = useShow<IBroker>({
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