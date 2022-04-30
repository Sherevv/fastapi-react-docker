import { useForm, Form, Input, Select, Edit, useSelect, RefreshButton, ListButton } from "@pankod/refine-antd";
import { IBroker, IPortfolio } from "interfaces";
import { useParams } from "react-router-dom";
import { HttpError } from "@pankod/refine-core";

export const PortfolioEdit: React.FC = () => {
    //let { action, id } = useParams();
    //let idd = id? id : '';
    const { formProps, saveButtonProps, queryResult } = useForm<IPortfolio,
        HttpError,
        IPortfolio>({
        //id: parseInt(idd),
        metaData:{
            fields: [
                "id",
                "name",
                {
                    broker: [
                        "id"
                    ],
                },
            ],
        },

    });

    const { selectProps: brokerSelectProps } = useSelect<IBroker>({
        resource: "brokers",
        metaData:{
            fields: [
                "id",
                "name",
            ],
        },
        optionLabel: "name",
        optionValue: "id",
        //defaultValue: queryResult?.data?.data?.broker?.id,
    });

    return (
        <Edit saveButtonProps={saveButtonProps}
              // pageHeaderProps={{ extra:
              //     <div>
              //         <ListButton />
              //         <RefreshButton onClick={() => queryResult?.refetch()} /></div> }}
        >
            <Form {...formProps} layout="vertical"
                  onFinish={(values) =>
                      formProps.onFinish?.({
                          ...values,
                          broker: values.broker.id,
                      } as any)
                  }>
                <Form.Item label="Name" name="name"
                           rules={[
                    {
                        required: true,
                    },
                ]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Broker" name={["broker", "id"]}>
                    <Select {...brokerSelectProps} />
                </Form.Item>
            </Form>
        </Edit>
    );
};