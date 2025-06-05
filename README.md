# aas-core-opc-ua
This repository provides OPC UA nodesets to represent the AAS meta-models.

The nodesets live in [nodesets/](nodesets/).

These OPC UA models allow us to reference AAS-specific data structures from within OPC UA.

Note, however, that they are not meant to represent AAS Submodel Templates in OPC UA.
The object types provided here strictly follow the AAS meta-model, which is not an optimal representation of data structures for AAS Submodel Templates.
For example, a `Property` AAS element with `valueType` set to `xs:string` is better represented as an OPC UA `String` rather than an `Property` object.

For the translation of AAS Submodel Templates to OPC UA nodesets, please see https://github.com/aas-core-works/aas-smt-codegen.

## Generation

The nodesets provided here are automatically generated using https://github.com/aas-core-works/aas-core-codegen.

For more details, see this publication:

```
@inproceedings{aasMeetsOpcUa,
  title     = {AAS Meets OPC UA: A Unified Approach to Digital Twins},
  author    = {Braunisch, Nico and Schmidt, Uwe and Proskurin, Erik and Ristin, Marko and Wollschlaeger, Martin and van de Venn, Hans Wernher and Bischoff, Tino},
  booktitle = {Proceedings of the {IEEE} International Conference on Industrial Cyber-Physical Systems ({ICPS})},
  year      = {2025},
  address   = {Emden, Germany}
}
```

You can request the full copy at: https://www.researchgate.net/publication/391862081_AAS_Meets_OPC_UA_A_Unified_Approach_to_Digital_Twins

## Contributing

If you want to contribute to the project in code, please see [CONTRIBUTING.md](CONTRIBUTING.md).
