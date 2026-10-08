#!/usr/bin/env bash

CSV_FILE="render_benchmark.csv"

rm -f "$CSV_FILE"
echo "Run,Samples,TotalRenderTime_Seconds,PeakMemory_MB" > "$CSV_FILE"

blender_cmd(){
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Error: Missing arguments."
        exit 1
    fi 

    prime-run ../blender/build_linux/bin/blender -b "$1"\
    -E CYCLES -P GPU_setup.py --python-expr "import bpy; bpy.context.scene.cycles.use_adaptive_sampling = False; bpy.context.scene.cycles.samples = $2" \
    -f 1 --debug-cycles -- --cycles-print-stats
}

for i in {1..50}; do
    if ((i > 25)); then
        SAMPLES=64
    else    
        SAMPLES=32
    fi

    RAW_OUTPUT=$(blender_cmd "test_scenes/repeat_zone_fractal_raymarch.blend" "$SAMPLES")
    
    render_time=$(echo "$RAW_OUTPUT" | grep "Total render time:" | awk '{print $NF}')   
    if [ -z "$render_time" ]; then
        render_time="FAILED"
    fi

    # Extract peak memory from the "Finished" line 
    peak_mem=$(echo "$RAW_OUTPUT" | grep "Finished" | grep -o "Mem: [0-9]*" | awk '{print $2}')
    if [ -z "$peak_mem" ]; then
        peak_mem="FAILED"
    fi

    # Write all values to the CSV file
    echo "$i,$SAMPLES,$render_time,$peak_mem" >> "$CSV_FILE"
    echo "Recorded Run $i: Time = ${render_time}s, Memory = ${peak_mem}MB"
done


