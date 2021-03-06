#   Copyright 2018 Samuel Payne sam_payne@byu.edu
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import covid19pandas as cod
import covid19pandas.exceptions as codex


formats = ("long", "wide")
jhu_data_types = ("all", "cases", "deaths", "recovered")
jhu_regions = ("global", "us")
update_options = (True, False)

nyt_data_types = ("all", "cases", "deaths")
nyt_county_options = (True, False)

# Test Johns Hopkins data getter
for format in formats:
    for data_type in jhu_data_types:
        for region in jhu_regions:
            for update_option in update_options:

                # Check that logic errors get caught
                if region == "us" and data_type == "recovered":
                    try:
                        cod.get_data_jhu(format=format, data_type=data_type, region=region, update=update_option)
                    except codex.ParameterError as e:
                        if str(e) != "JHU does not provide recovery data for US states/counties.":
                            raise Exception(f"Test failed. format='{format}', data_type='{data_type}', region='{region}', update='{update_option}'")
                        else:
                            print(f"Logic error successfully caught! format='{format}', data_type='{data_type}', region='{region}', update='{update_option}'")

                elif format == "wide" and data_type == "all":
                    try:
                        cod.get_data_jhu(format=format, data_type=data_type, region=region, update=update_option)
                    except codex.ParameterError as e:
                        if str(e) != "'wide' table format only allows one data type. You requested 'all'. Please pass 'cases', 'deaths', or 'recovered'.":
                            raise Exception(f"Test failed. format='{format}', data_type='{data_type}', region='{region}', update='{update_option}'")
                        else:
                            print(f"Logic error successfully caught! format='{format}', data_type='{data_type}', region='{region}', update='{update_option}'")
                else:
                    df = cod.get_data_jhu(format=format, data_type=data_type, region=region, update=update_option)
                    if df.shape[0] <= 0 or df.shape[1] <=0:
                        raise Exception(f"Dataframe had zero in shape: {df.shape}")
                    print(f"Success! format='{format}', data_type='{data_type}', region='{region}', update='{update_option}, returned {df.shape}'")

# Test New York Times data getter
for format in formats:
    for data_type in nyt_data_types:
        for county_option in nyt_county_options:
            for update_option in update_options:

                # Check that logic errors get caught
                if format == "wide" and data_type == "all":
                    try:
                        cod.get_data_nyt(format=format, data_type=data_type, counties=county_option, update=update_option)
                    except codex.ParameterError as e:
                        if str(e) != "'wide' table format only allows one data type. You requested 'all'. Please pass 'cases', 'deaths', or 'recovered'.":
                            raise Exception(f"Test failed. format='{format}', data_type='{data_type}', counties='{county_option}', update='{update_option}'")
                        else:
                            print(f"Logic error successfully caught! format='{format}', data_type='{data_type}', counties='{county_option}', update='{update_option}'")
                else:
                    df = cod.get_data_nyt(format=format, data_type=data_type, counties=county_option, update=update_option)
                    if df.shape[0] <= 0 or df.shape[1] <=0:
                        raise Exception(f"Dataframe had zero in shape: {df.shape}")
                    print(f"Success! format='{format}', data_type='{data_type}', counties='{county_option}', update='{update_option}, returned {df.shape}'")

# Test deprecated getters
df = cod.get_cases()
if df.shape[0] <= 0 or df.shape[1] <=0:
    raise Exception(f"Dataframe had zero in shape: {df.shape}")
print(f"Success with deprecated get_cases method. Returned {df.shape}.")
df = cod.get_deaths()
if df.shape[0] <= 0 or df.shape[1] <=0:
    raise Exception(f"Dataframe had zero in shape: {df.shape}")
print(f"Success with deprecated get_deaths method. Returned {df.shape}.")
df = cod.get_recovered()
if df.shape[0] <= 0 or df.shape[1] <=0:
    raise Exception(f"Dataframe had zero in shape: {df.shape}")
print(f"Success with deprecated get_recovered method. Returned {df.shape}.")
