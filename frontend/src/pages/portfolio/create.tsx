import {
    Create,
    Form,
    Input,
    Select,
    useForm,
    useSelect,
} from "@pankod/refine-antd";

import { IBroker, IPortfolio } from "interfaces";
import { HttpError } from "@pankod/refine-core";

export const PortfolioCreate = () => {
    const { formProps, saveButtonProps } = useForm<IPortfolio,
        HttpError,
        IPortfolio>(
        {
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
    });

    return (
        <Create saveButtonProps={saveButtonProps}>
            <Form {...formProps} layout="vertical"
                  onFinish={(values) =>{
                      if (values.broker){
                          values = {...values,
                              brokerId: values.broker.id,
                          } as any;
                          delete values.broker;
                      }
                      formProps.onFinish?.(values);
                  }}>
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
        </Create>
    );
};
