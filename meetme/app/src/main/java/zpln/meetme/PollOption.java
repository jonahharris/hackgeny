package zpln.meetme;

import android.util.JsonReader;

import java.io.IOException;

/**
 * Created by tamar on 6/12/2015.
 */
public class PollOption {
    private int pollOptionId;
    private String pollOptionName;

    private int pollOptionCount;

    public PollOption(int pollOptionId, String pollOptionName, int pollOptionCount){
        this.pollOptionId = pollOptionId;
        this.pollOptionName = pollOptionName;
        this.pollOptionCount = pollOptionCount;
    }

    public PollOption(String pollOptionName) {
        this.pollOptionId = -1;
        this.pollOptionName = pollOptionName;
        this.pollOptionCount = -1;
    }

    public PollOption(JsonReader reader) throws IOException {
        this.pollOptionId = -1;
        this.pollOptionName = null;
        this.pollOptionCount = -1;

        reader.beginObject();
        while (reader.hasNext()) {
            String name = reader.nextName();
            if (name.equals("poll_option_id")) {
                this.pollOptionId = reader.nextInt();
            } else if (name.equals("poll_option_name")) {
                this.pollOptionName = reader.nextString();
            } else if (name.equals("poll_option_count")) {
                this.pollOptionCount = reader.nextInt();
            } else {
                reader.skipValue();
            }
        }
        reader.endObject();
    }

    public int getPollOptionId() {
        return pollOptionId;
    }

    public String getPollOptionName() {
        return this.pollOptionName;
    }

    public int getPollOptionCount() { return pollOptionCount; }
}
